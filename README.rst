cloud-formation-viz
===================

This tool is for creating visualizations of CloudFormation templates.
It outputs Graphviz dot files. It can be used like this::

    cat example.template | ./cfviz | dot -Tsvg -oexample.svg


The only dependency of the `cfviz` script is Python. You will also
need to have Graphviz_  installed for the output to be any use.

The samples_ directory contains output of running the tool
over the aws-samples_ provided by AWS.

.. _aws-samples: http://aws.amazon.com/cloudformation/aws-cloudformation-templates/
.. _Graphviz: http://www.graphviz.org/
.. _samples: https://github.com/benbc/cloud-formation-viz/tree/master/samples
