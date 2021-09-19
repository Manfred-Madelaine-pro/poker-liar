
class Statistics:
    def __init__(self):
        self.lied = []
        self.accused = []
        self.accusations = []

        self.worst_loss = 0
        self.best_escape = 0
        self.total_cards_exchanged = 0

    def __str__(self):
        return f"lied: {self.lied}\tdenouncing: {self.accusations}\tdenounced: {self.accused}"

    def stats(self):
        lies = self.lied.count(True)
        truths = self.lied.count(False)

        legitimately = self.accused.count(True)
        wrongly = self.accused.count(False)

        correct = self.accusations.count(True)
        incorrect = self.accusations.count(False)

        txt = ""
        if self.lied:
            txt += f"lies VS Truths: {lies} ({round((lies/len(self.lied))*100, 1)}%) VS {truths} ({round((truths/len(self.lied))*100, 1)}%)\t"
        if self.accused:
            txt += f"Legitimately VS Wrongly accused: {legitimately} ({round((legitimately/len(self.accused))*100, 1)}%)) VS "
            txt += f"{wrongly} ({round((wrongly/len(self.accused))*100, 1)}%))\t"
        if self.accusations:
            txt += f"Correct VS Incorrect accusations: {correct} ({round((correct/len(self.accusations))*100, 1)}%)) VS "
            txt += f"{incorrect} ({round((incorrect/len(self.accusations))*100, 1)}%))"
        return txt
