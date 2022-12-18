# Shortcut: Send URL to Omnifocus

Runs [Get A URL](./get-a-url.md) to get one or more URLs. For each URL:

* Runs `automate-jw-process-url`, passing the URL
* If the result begins with `omnifocus`
    - Strip `omnifocus ` from the start
    - Base64 encode if looks like JSON
    - Runs a script to process string and create an Omnifocus task

## Status
* Creates Omnifocus tasks
* Next steps: split the Omnifocus part into own Shortcut

## Commands

Commands are plain text, variables are **in bold**, multiple variables are **split** `_` **with an underscore**.

* Takes a File Path: path to `automatic-jw-process-url`, preferably in a virtual environment with 3rd-party libraries installed.
* Run **[Get a URL](./get-a-url.md)**
* Repeat with each item in **Shortcut Result**
    - Run Shell Script
      **File Path** " **Repeat Item** "
      Shell **sh**
      Input **Repeat Item**
      Pass Input **as arguments**
      Do not run as administrator
    - If **Shell Script Result** `_` **begins with** `_` **omnifocus**
        - Replace **`^omnifocus `** (*omnifocus as start of line with a space*) with **World** (*nothing*) in **Shell Script Result**
        - If **Updated Text** `_` **begins with** `_` **{**
            - **Encode** `_` **Updated Text** with base64
            - Set variable **omnidata** to **Base64 Encoded**
        - Otherwise
            - Set variable **omnidata** to **Updated Text**
        - End If
        - Run a script with **omnidata** via Omni Automation
          *see below for script*
    - Otherwise
        - Show **Shell Script Result** in Quick Look
    - End If
- End Repeat

### OmniAutomation Script

```
var input_txt = `omnidata`.trim()
var raw_txt = Data.fromBase64(input_txt).toString()
var data = JSON.parse(raw_txt)
var project = null
var issues = new Array()

if (data.project) {
  var project = flattenedProjects.byName(data.project)
  if (!project) {
     issues.push(`Unknown project "${data.project}"`)
  }
}

var task = new Task(data.task, project)

if (data.flag) {
  task.flagged = true
}

if (data.tags && data.tags.length) {
  for (const tagName of data.tags) {
    var tag = flattenedTags.byName(tagName)
    if (tag) {
      task.addTag(tag)
    } else {
      issues.push(`Unknown tag "${tagName}"`)
    }
  }
}
if (data.start_date) {
  // Set start date
}
if (data.end_date) {
  // Set end date
}
if (data.estimate) {
  // Set estimate
}

// Determine the note
var note = ""
if (data.note) {
  note = data.note
}
if (issues && issues.length) {
  console.log(issues)
  if (note) {
    note += "\n\n"
  }
  note += "IMPORT ISSUES\n"
  note += issues.join("\n")
  note += "\nEND OF IMPORT ISSUES\n"
}

// Debug
note += "\n\nINPUT JSON\n"
note += raw_txt
note += "\nEND OF INPUT JSON\n"

if (note) {
  task.note = note
}

var taskID = task.id.primaryKey
URL.fromString("omnifocus:///task/" + taskID).open()
if (note) {
  if (project) {
    window = document.windows[0]
    window.perspective = Perspective.BuiltIn.Projects
  }
  tree = document.windows[0].content
  node = tree.nodeForObject(task)
  if (node) {
    node.expandNote()
  }
}
```
