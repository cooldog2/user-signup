
import webapp2
import re

form = """
<form method="post">
    <table>
        <tr>
            <td>
                <label> Username <input type="text" name="username" value="%(username)s" required=""> </label>
                <span style="color: red">%(error_username)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label> Password <input type="password" name="password" > </label>
                <span style="color: red">%(error_password)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label> Verify Password <input type="password" name="verify" > </label>
                <span style="color: red">%(error_validation)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label> Email (optional) <input type="email" name="email" value="%(email)s"> </label>
                <span style="color: red">%(error_email)s</span><br>
            </td>
        </tr>
    </table>
    <input type="submit"/>
</form>
"""
#user cannot contain spaces
# def valid_username(username):
#     if "" not in username:
#         return username

username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username_regex.match(username) and username

# def valid_password(password):
#     if "" not in password:
#         return password

password_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password_regex.match(password) and password

# def valid_verification(verify):
#     if verify == password:
#         return verify


# def valid_email(email):
#         return email  #need to define logic

email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return email_regex.match(email) or not email

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.user-input.com/
    """
    def write_form(self, error_username="",error_password="", error_validation="",
        error_email="", username="", email=""):
        self.response.out.write(form % {"error_username": error_username,
                                    "error_password": error_password,
                                    "error_validation": error_validation,
                                    "error_email": error_email,
                                    "username": username,
                                    "email": email})

    def get(self):
        self.write_form()

    def post(self):

        have_error=False

        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_verification = self.request.get('verify')
        user_email = self.request.get('email')

        # username = valid_username(self.request.get("username"))
        # password = valid_password(self.request.get("password"))
        # verification = valid_verification(self.request.get("verify"))
        # email = valid_email(self.request.get("email"))

        #if user did not complete form correctly, re-render form
        error_username=""
        error_password=""
        error_validation=""
        error_mail=""

        if not valid_username(user_name):
            error_username ="That is not a valid username"
            have_error=True

        if not valid_password(user_password):
            error_password = "That is not a valid password"
            have_error=True

        elif user_password != user_verification:
            error_validation = "The passwords do not match"
            have_error=True
        if not valid_email(user_email):
            error_email = "That is not a valid email."
            have_error=True
        if have_error:
            self.write_form(error_username, error_password, error_validation,error_mail, user_name, user_email)

        else:
            username = self.request.get('username')
            self.redirect('/welcome?username=%s' % username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome " + username)

app = webapp2.WSGIApplication([('/', MainHandler), ('/welcome',Welcome)], debug=True)
