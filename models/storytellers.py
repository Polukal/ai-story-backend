from db import db

class Storyteller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    tone = db.Column(db.String(50))
    plot_setup = db.Column(db.Text)
    visual_style = db.Column(db.String(50))
    image_url = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "genre": self.genre,
            "tone": self.tone,
            "plot_setup": self.plot_setup,
            "visual_style": self.visual_style,
            "image_url": self.image_url,
        }
