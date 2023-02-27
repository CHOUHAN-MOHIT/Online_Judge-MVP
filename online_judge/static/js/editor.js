// Custom javascript




//Ace configuration
let defaltValue = '#include<bits/stdc++.h>\nusing namespace std;\n\nint main(){\n\n\treturn 0;\n}';

let codeEditor = ace.edit("editorCode");
let editorLib = {
    init() {
        
        codeEditor.setTheme("ace/theme/twilight");
        codeEditor.session.setMode("ace/mode/c_cpp");
        codeEditor.setValue(defaltValue)
    }
}

editorLib.init()

