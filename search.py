import os
import sublime, sublime_plugin

view_prename = "search files for:"

class OpenFileSearchUnderSelectedCommand(sublime_plugin.TextCommand):
    def run(self, edit):    
    	if view_prename not in self.view.name():
    		return	    

        sel = self.view.sel()[0] 
        if not sel.empty():
            file_name = self.view.substr(sel)
        else:
            caret_pos = self.view.sel()[0].begin()
            current_line = self.view.line(caret_pos)

            left = current_line.begin()
            right = current_line.end()
            file_name = self.view.substr(sublime.Region(left, right))

        print str(file_name	)        
        file_name = file_name.strip()

        if os.path.exists(file_name) and os.path.isfile(file_name):
            self.view.window().open_file(file_name)
            

class EverythingSearchCommand(sublime_plugin.WindowCommand):
	
	def run(self):				
		self.window.show_input_panel("Search files:", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		view = self.window.new_file()
		view.set_name(view_prename+text)
		f=os.popen("es -n 100 -r " + text.encode('gbk'))					
		edit = view.begin_edit()  
		result = ""
		count = 0
		for l in f.readlines():     					
			result += self.decodeText(l)
			count += 1

		result += "\n" + str(count) +" result"
		view.insert(edit, 0, result)
		view.end_edit(edit)


	def decodeText(self, text):
		result = ""
		try:
			result = text.decode('gbk')
		except:
			result = "Error Codec\n"
		return result
