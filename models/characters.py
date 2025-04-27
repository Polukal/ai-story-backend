from db import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    traits = db.Column(db.String(200))
    backstory = db.Column(db.Text)
    image_url = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "traits": self.traits,
            "backstory": self.backstory,
            "image_url": self.image_url,
        }
