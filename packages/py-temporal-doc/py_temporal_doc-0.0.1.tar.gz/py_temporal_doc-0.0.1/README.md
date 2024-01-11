# py-temporal-doc

### Sample json structure

```
{
  "callers": {
    "Periodic": {
        "data": ["Workflow1", "Workflow2"],
        "docstring": "comment...",
        "path": "project.directory.file.py"
    },
    "PostMethod": {
        "workflows": ["Workflow3", "Workflow4"],
        "docstring": "comment...",
        "path": "project.directory.file.py"
    }
  },
  "workflows": {
    "Workflow1": {
      "data": [
        "ChildWorkflow1",
        "Activity1", 
        "ChildWorkflow2", 
        "Activity2"
      ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    },
    "Workflow2": {
      "sequence": [
        "Activity2", 
        "Activity3"
      ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    },
    "Workflow3": {
      "sequence": [
        "Activity3", 
        "Activity4"
            ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    },
    "Workflow4": {
      "sequence": [
        "Activity4"
      ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    },
    "ChildWorkflow1": {
      "sequence": [
        "Activity1"
      ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    },
    "ChildWorkflow2": {
      "sequence": [
        "Activity2"
      ],
      "docstring": "comment...",
      "path": "project.directory.file.py"
    }
  },
  "activities": {
    "Activity1": {
        "docstring": "comment...",
        "path": "project.directory.file.py"
    },
    "Activity2": {
        "docstring": "comment...",
        "path": "project.directory.file.py"
    },
    "Activity3": {
        "docstring": "comment...",
        "path": "project.directory.file.py"
    },
    "Activity4": {
        "docstring": "comment...",
        "path": "project.directory.file.py"
    }
  }
}
```

### Decorator Usage

```
@activity.defn
async def activity1() -> None:
    pass
    
@activity.defn
async def activity2() -> None:
    pass
    
@activity.defn
async def child_activity1() -> None:
    pass
    
@activity.defn
async def child_activity2() -> None:
    pass

@document.workflow_sequence(
    child_activity1
)
@workflow.defn
class ChildWorkflow1:

    @workflow.run
    async def run(self) -> None:    
        pass
        

@document.workflow_sequence(
    child_activity2
)  
@workflow.defn
class ChildWorkflow2:

    @workflow.run
    async def run(self) -> None:    
        pass
        
        
@document.workflow_sequence( # Decorator to indicate the sequence of activities and child workflows inside a workflow
    activity1,
    ChildWorkflow1,
    activity2,
    ChildWorkflow2
)
@workflow.defn
class Workflow1:

    @workflow.run
    async def run(self) -> None:    
        pass
        

@document.workflow_sequence(
    ChildWorkflow1,
    ChildWorkflow2
)  
@workflow.defn
class Workflow2:

    @workflow.run
    async def run(self) -> None:    
        pass
       
        
@document.workflow_caller( # Decorator to indicate the starting point on when the workflows are called
    Workflow1,
)
def call_worklow1():
    client = await temporal_client(namespace=TEMPORAL_NAMESPACE)
    
    await temporal.execute_workflow(
        Workflow1.run,
        ...
    )
    
@document.workflow_caller(
    Workflow2
)
def call_worklow2():
    client = await temporal_client(namespace=TEMPORAL_NAMESPACE)
    
    await temporal.execute_workflow(
        Workflow2.run,
        ...
    )

```

### How to run
```
python main.py generate-json <path>
```