from aws_cdk.core import App

from stack.hello_workflow_stack import HelloWorkflowStack


app = App()
HelloWorkflowStack(app, "HelloWorkflowStack")
app.synth()
