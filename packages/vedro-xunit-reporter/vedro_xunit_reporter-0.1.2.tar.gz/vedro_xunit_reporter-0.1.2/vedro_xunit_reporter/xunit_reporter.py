import os
import socket
from datetime import datetime, timezone
from pathlib import Path
from traceback import format_exception
from typing import Type, Union
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from vedro.core import Dispatcher, ExcInfo, PluginConfig, ScenarioResult
from vedro.events import (ArgParsedEvent, ArgParseEvent, CleanupEvent,
                          ScenarioReportedEvent, StartupEvent)
from vedro.plugins.director import DirectorInitEvent, Reporter

__all__ = ("XUnitReporterPlugin", "XUnitReporter",)


class XUnitReporterPlugin(Reporter):
    def __init__(self, config: Type["XUnitReporter"]):
        super().__init__(config)
        self._report_path = config.report_path
        self._include_skipped = config.include_skipped
        self._test_suites: Union[Element, None] = None
        self._test_suite: Union[Element, None] = None

    def subscribe(self, dispatcher: Dispatcher) -> None:
        super().subscribe(dispatcher)
        dispatcher.listen(DirectorInitEvent, lambda e: e.director.register("xunit", self))

    def on_chosen(self) -> None:
        assert isinstance(self._dispatcher, Dispatcher)
        self._dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                        .listen(ArgParsedEvent, self.on_arg_parsed) \
                        .listen(StartupEvent, self.on_startup) \
                        .listen(ScenarioReportedEvent, self.on_scenario_reported) \
                        .listen(CleanupEvent, self.on_cleanup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("XUnit Reporter")
        group.add_argument("--xunit-report-path", type=Path, default=self._report_path,
                           help=f"Path to save the xUnit report (default: '{self._report_path}')")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._report_path = event.args.xunit_report_path

    def on_startup(self, event: StartupEvent) -> None:
        self._test_suites = Element("testsuites")
        self._test_suite = SubElement(self._test_suites, "testsuite",
                                      name="Scenarios", hostname=socket.gethostname())

    def on_scenario_reported(self, event: ScenarioReportedEvent) -> None:
        assert self._test_suite is not None
        test_case = self._add_test_case(event.aggregated_result, self._test_suite)

        if event.aggregated_result.is_failed():
            for step_result in event.aggregated_result.step_results:
                if step_result.exc_info:
                    self._add_failure(step_result.exc_info, test_case)
                    return
        elif event.aggregated_result.is_skipped() and self._include_skipped:
            self._add_skipped(test_case)

    def _add_test_case(self, scenario_result: ScenarioResult,
                       test_suite: Element) -> Element:
        scenario = scenario_result.scenario
        classname = self._path_to_module(scenario.rel_path) + f".{scenario.name}"
        return SubElement(test_suite, "testcase", {
            "name": scenario.subject,
            "classname": classname,
            "time": f"{scenario_result.elapsed:.3f}",
        })

    def _add_failure(self, exc_info: ExcInfo, test_case: Element) -> Element:
        failure = SubElement(test_case, "failure", {
            "type": str(exc_info.type.__name__),
            "message": str(exc_info.value),
        })
        if exc_info.traceback:
            traceback = exc_info.traceback
            failure.text = "".join(format_exception(exc_info.type, exc_info.value, traceback))
        return failure

    def _add_skipped(self, test_case: Element) -> Element:
        return SubElement(test_case, "skipped")

    def _path_to_module(self, path: Path) -> str:
        return str(path).replace(os.sep, ".")[:-len(path.suffix)]

    def _timestamp_to_iso8601(self, started_at: float) -> str:
        dt = datetime.fromtimestamp(started_at, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

    def _save_report(self, xml_report: bytes) -> None:
        result = minidom.parseString(xml_report).toprettyxml()
        try:
            with open(self._report_path, "w") as f:
                f.write(result)
        except IOError:
            raise

    def on_cleanup(self, event: CleanupEvent) -> None:
        assert self._test_suites is not None
        assert self._test_suite is not None

        report = event.report
        started_at = self._timestamp_to_iso8601(report.started_at if report.started_at else 0.0)

        self._test_suite.set("timestamp", started_at)
        self._test_suite.set("time", f"{report.elapsed:.3f}")
        self._test_suite.set("tests", f"{report.total}")
        self._test_suite.set("failures", f"{report.failed}")
        self._test_suite.set("skipped", f"{report.skipped}")
        self._test_suite.set("errors", "0")

        xml_report = tostring(self._test_suites)
        self._save_report(xml_report)


class XUnitReporter(PluginConfig):
    plugin = XUnitReporterPlugin
    description = "xUnit format reporter for Vedro testing framework"

    # Path to save the xUnit report
    report_path: Path = Path("./xunit_report.xml")

    # Include skipped scenarios in the report
    include_skipped: bool = True
