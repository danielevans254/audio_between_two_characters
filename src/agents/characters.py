class CharacterAgent:
    def __init__(self, name, script):
        self.name = name
        self.script = script
        self.current_line = 0

    def speak(self):
        if self.current_line < len(self.script):
            line, audio = self.script[self.current_line]
            self.current_line += 1
            return line, audio
        return None, None
