::@ECHO OFF
call pyuic4 "qt\ui\editor.ui" -o "ui_editor.py"

call pyuic4 "qt\ui\anagram.ui" -o "ui_anagram.py"
call pyuic4 "qt\ui\diffs.ui" -o "ui_diffs.py"
call pyuic4 "qt\ui\eboot.ui" -o "ui_eboot.py"
call pyuic4 "qt\ui\fontgen.ui" -o "ui_fontgenerator.py"
call pyuic4 "qt\ui\fontgenwidget.ui" -o "ui_fontgenwidget.py"
call pyuic4 "qt\ui\modeleditor.ui" -o "ui_modeleditor.py"
call pyuic4 "qt\ui\nonstop.ui" -o "ui_nonstop.py"
call pyuic4 "qt\ui\openmenu.ui" -o "ui_open.py"
call pyuic4 "qt\ui\search.ui" -o "ui_search.py"
call pyuic4 "qt\ui\settings.ui" -o "ui_settings.py"
call pyuic4 "qt\ui\terminology.ui" -o "ui_terminology.py"
call pyuic4 "qt\ui\termedit.ui" -o "ui_termedit.py"
call pyuic4 "qt\ui\wizard.ui" -o "ui_wizard.py"

call pyrcc4 "qt\res\icons.qrc" -o "icons_rc.py"