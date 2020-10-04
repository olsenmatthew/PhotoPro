import psycopg2
import time


def create_user(first, last, email, password, conn, cur):
	try:
		cmd = "INSERT INTO users(first,last,email,password) VALUES('{}','{}','{}', '{}');".format(first, last, email,
																								  password)
		print(cmd)
		cur.execute(cmd)
		conn.commit()
		return "Welcome {} {}".format(first, last)
	except psycopg2.errors.UniqueViolation as e:
		print(e)
		return "Unable to create new account. Account with that email already exists."


def login_user(email, password, conn, cur):
	cmd = "SELECT * FROM users WHERE email='{}' AND password='{}'".format(email, password)
	print(cmd)
	cur.execute(cmd)
	conn.commit()
	data = cur.fetchall()
	length = len(data)
	if length == 0:
		return "Incorrect email or password! Please try again."
	elif length == 1:
		(id, first, last, email, password) = data[0]
		print(id, first, last, email, password)
		return "Welcome back {} {}".format(first, last)
	else:
		print("Email not unique")


def change_password(email, password, new_password, conn, cur):
	login_response = login_user(email, password, conn, cur)

	if "Welcome back" in login_response:
		cmd = "UPDATE users SET password = '{}' WHERE email='{}' AND password='{}'".format(
			new_password,
			email,
			password
		)
		print(cmd)
		cur.execute(cmd)
		conn.commit()
		return "Successfully changed password!"
	else:
		return login_response


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl


def forgot_password_get_change_password_link(recipient, conn, cur):
	cmd = "SELECT * FROM users WHERE email='{}'".format(email)
	print(cmd)
	cur.execute(cmd)
	conn.commit()
	data = cur.fetchall()
	length = len(data)
	if length == 0:
		return "Incorrect email or password! Please try again."
	elif length == 1:
		ssl_port = 587
		email_server_password = 'WeCodeNotSleep3900'
		context = ssl.create_default_context()
		with smtplib.SMTP("smtp.gmail.com", ssl_port) as server:
			server.ehlo()
			server.starttls(context=context)
			sender = "2mjec390@gmail.com"

			message = MIMEMultipart("alternative")
			message['Subject'] = "PhotoPro: Reset Your Password"
			message['From'] = sender
			message['To'] = recipient
			reset_url = "www.photopro.com/reset-password/id"

			html = "\
				<html>\
					<body>\
						<p> Need to reset your password? <br>\
						You can do this easily using the link below: <br>\
								<center>{}</center> <br>\
						If you didn't ask to reset your password, please get in touch at support@photopro.com. <br>\
						</p>\
					</body>\
				</html>".format(reset_url)
			html = MIMEText(html, 'html')
			message.attach(html)

			server.login("2mjec390@gmail.com", email_server_password)
			server.sendmail(sender, recipient, message.as_string())

			return "Your email has just sent a link to change your password. Make sure to check your spam folder!"
	else:
		print("Email not unique")


if __name__ == '__main__':
	port = 5432
	host = '34.87.239.111'
	database_user = 'outside_user'
	database_password = 'outside_user'
	database_name = 'postgres'

	conn = psycopg2.connect(user=database_user, password=database_password,
							host=host, port=port, database=database_name)
	cur = conn.cursor()

	print(conn, cur)

	table = "users"
	first = 'Matthew'
	last = 'Olsen'
	email = 'olsenmatthew780@gmail.com'
	password = 'password'

	# response = create_user(first, last, email, password, conn, cur)
	# print(response)

	# time.sleep(1)
	#
	# response = login_user(email, password, conn, cur)
	# print(response)

	# response = change_password(email, password, "new_password", conn, cur)
	# print(response)

	response = forgot_password_get_change_password_link(email, conn, cur)
	print(response)

	if conn:
		cur.close()
		conn.close()