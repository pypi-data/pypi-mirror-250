# Summary

[`pmlib`][1] is a library to leverage [`TaskWarrior`][2] to track and manage projects.

[`pmlib`][1] requires adds per-task project owners, which are a basic requirement of any project tracking system.  The original [`TaskWarrior`][2] concept assumes all tasks are owned by the user running TaskWarrior.

# Installation

- Install [TaskWarrior][2]
- `pip install pmlib`

# Gantt Chart

[![gantt_image](https://github.com/mpenning/pmlib/blob/main/docs/gantt.png)](https://github.com/mpenning/pmlib/blob/main/docs/gantt.png)

# Usage

Assume you want to create nine tasks, eight of which are dependencies of the first task:

```python
from pmlib.task import OwnedTask
from pmlib.task import OwnedTaskWarrior

otw = OwnedTaskWarrior(data_location="~/.pm", create=True, purge_existing=False)
otw.purge_project("version_1.6.0")
task01 = OwnedTask(otw,
                   description="Complete software version 1.6.0",
                   start="2023-12-01",
                   due="2024-01-26",
                   project="version_1.6.0",
                   owner="pm@gmail.com")
task02 = OwnedTask(otw,
                   description="Fix bugs for version 1.6.0",
                   start="2023-12-01",
                   due="2023-12-21",
                   project="version_1.6.0",
                   status="completed",
                   owner="dev02@gmail.com")
task03 = OwnedTask(otw,
                   description="Rewrite PDF exporter",
                   start="2023-12-01",
                   due="2023-12-15",
                   project="version_1.6.0",
                   owner="dev01@gmail.com",
                   status="pending")
task04 = OwnedTask(otw,
                   description="Test PDF exporter",
                   start="2023-12-15",
                   due="2024-01-05",
                   project="version_1.6.0",
                   owner="test01@gmail.com")
task05 = OwnedTask(otw,
                   description="Write feature for print driver",
                   start="2023-12-15",
                   due="2023-12-19",
                   project="version_1.6.0",
                   owner="dev01@gmail.com")
task06 = OwnedTask(otw,
                   description="Test print driver",
                   start="2023-12-19",
                   due="2023-12-27",
                   project="version_1.6.0",
                   owner="test01@gmail.com")
task07 = OwnedTask(otw,
                   description="Build new version 1.6.0 binary",
                   start="2023-12-27",
                   due="2024-01-06",
                   project="version_1.6.0",
                   owner="builder01@gmail.com")
task08 = OwnedTask(otw,
                   description="Test new version 1.6.0 binary",
                   start="2023-12-27",
                   due="2024-01-06",
                   project="version_1.6.0",
                   owner="test01@gmail.com")
task09 = OwnedTask(otw,
                   description="Write version 1.6.0 release notes",
                   start="2023-12-27",
                   due="2024-01-16",
                   project="version_1.6.0",
                   owner="techwriter01@gmail.com")
task02.save()
task03.save()
task04.save()
task05.save()
task06.save()
task07.save()
task08.save()
task09.save()
task01.set_depends([task02, task03, task04, task05, task06, task07, task08, task09])
task01.save()

# This should be True, newtask02 is in the list of dependencies
#print(task02 in task01['depends'])

otw.save_project_gantt_chart("version_1.6.0", "gantt.png")

# Print a task table wrapped to 100 characters wide...
print(otw.get_table(100))
```

That will print (task UUIDs will be different):

```none
      uuid                due          depends        owner            project        description
====================================================================================================
3b6a4d97-7c22-      2023-12-15         0         dev01@gmail.com    version_1.6.0   Rewrite PDF
4eb4-8085-          00:00:00-06:00                                                  exporter
83cacf1da997
c63804e1-631a-      2024-01-05         0         test01@gmail.com   version_1.6.0   Test PDF
473f-8770-          00:00:00-06:00                                                  exporter
f1b1320f3dab
24569bde-4f30-      2023-12-19         0         dev01@gmail.com    version_1.6.0   Write feature
4666-9f38-          00:00:00-06:00                                                  for print driver
89c400a73c6f
161b1e4a-d770-      2023-12-27         0         test01@gmail.com   version_1.6.0   Test print
48d2-a5ca-          00:00:00-06:00                                                  driver
7b2f36837c5f
884f388b-2366-      2024-01-06         0         builder01@gmail.   version_1.6.0   Build new
4633-98a0-          00:00:00-06:00               com                                version 1.6.0
423509bc5fa6                                                                        binary
46cace11-a340-      2024-01-06         0         test01@gmail.com   version_1.6.0   Test new version
4a18-8ce2-          00:00:00-06:00                                                  1.6.0 binary
d02aa7f5c0c1
7c7c2b01-9794-      2024-01-16         0         techwriter01@gma   version_1.6.0   Write version
4e79-bea2-          00:00:00-06:00               il.com                             1.6.0 release
37662b016204                                                                        notes
35b4ed99-2461-      2024-01-26         8         pm@gmail.com       version_1.6.0   Complete
4d89-9304-          00:00:00-06:00                                                  software version
81fc21ad3148                                                                        1.6.0
14cd59d4-2037-      2023-12-21         0         dev02@gmail.com    version_1.6.0   Fix bugs for
49cc-8b39-          00:00:00-06:00                                                  version 1.6.0
9ad9b9863f4e
```

 [1]: https://github.com/mpenning/pmlib
 [2]: https://github.com/GothenburgBitFactory/taskwarrior

