# Vedro xUnit Reporter

`vedro-xunit-reporter` is a plugin for the Vedro testing framework that generates test reports in the xUnit XML format. This plugin allows you to easily integrate your Vedro tests with various Continuous Integration (CI) systems and tools that support xUnit report format.

## Installation

To install `vedro-xunit-reporter`, you can use the `vedro plugin install` command:

```sh
$ vedro plugin install vedro-xunit-reporter
```

Ensure you have Vedro already installed in your environment. If not, you can install it using pip:

```sh
$ pip install vedro
```

## Usage

To generate an xUnit report, run your Vedro tests with the `-r` (reporter) option, specifying `xunit` as the reporter:

```sh
$ vedro run -r rich xunit
```

This command will execute your tests and generate an xUnit report. By default, the report is saved to `./xunit_report.xml` in your project directory.
