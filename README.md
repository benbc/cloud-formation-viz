cloud-formation-viz
===================

This tool is for creating visualizations of CloudFormation templates.

Installation:
```` bash
cd cloud-formation-viz
python -m venv .venv 
source .venv/bin/activate
python setup.py install
````

It outputs Graphviz dot files. It can be used like this where 
example.template is a json cloudformation template:
```` bash
cat example.template | cfviz | dot -Tsvg -oexample.svg
````

The following can be used with yaml formatted templates:
```` bash
cfviz example.yaml | dot -Tsvg -oexample.svg
````

The only dependency of the `cfviz` script is Python (>=3.7) and the PyYaml 
package. You will also need to have [Graphviz] [graphviz] installed for the 
output to be any use.

The [samples] [samples] directory contains output of running the tool
over the [samples] [aws-samples] provided by AWS.

[aws-samples]: http://aws.amazon.com/cloudformation/aws-cloudformation-templates/
[graphviz]: http://www.graphviz.org/
[samples]: https://github.com/benbc/cloud-formation-viz/tree/master/samples
