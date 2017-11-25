

    def eventShowLists(self):
        self.data_keys_for_buts = []
        
        text = QTextEdit()
        
        self.got_data = App.getData(self)

        with self.got_data:
            data_keys = self.got_data.variables.keys()
            for k in data_keys:
                self.lbl = k
                self.data_keys_for_buts.append(k)
                str_param = '\n'.join(self.data_keys_for_buts)
        
        text.setLabelText(str_param)
        return  text.show()
