class Menulink():

    def __init__(self, text, href, css_class):
        self.text = text
        self.href = href
        self.css_class = css_class

    @classmethod
    def home(cls):
        return [cls(text="Apply to CODECOOL", href="applicant_apply", css_class="highlight"),
                cls(text="Applicant login", href="applicant_login", css_class="normal"),
                cls(text="Mentor login", href="homepage", css_class="normal"),
                cls(text="Admin login", href="admin_login", css_class="normal")]

    @classmethod
    def admin(cls):
        return [cls(text="Filter Applicants", href="admin_page", css_class="normal"),
                cls(text="Logout", href="logout", css_class="logout")]

    @classmethod
    def applicant(cls):
        return [cls(text="My profile", href="applicant_profile", css_class="normal"),
                cls(text="My interview", href="applicant_interview", css_class="normal"),
                cls(text="Logout", href="applicant_logout", css_class="logout")]
