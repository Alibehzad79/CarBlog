# CarBlog
<h1>The Blog with django</h1>
-------------------------------------- <br />
open Terminal in Linux and mac , cmd in windows

<h6>Install Virtualenv</h6>
pip install virtualenv <br />
mkdir CarBlog <br />
--> virtualenv venv <br />
--------------------------------------
<h6>clone CarBlog to CarBlog folder in your pc</h6>
cd CarBlog/CarBlog
<br />
<ol type='a'>
  <li>pip install -r requirements.txt</li>
  <li>python manage.py migrate</li>
  <li>python manage.py collectstatic</li>
  <li>python manage.py createsuperuser  ::: # for login</li>
  <li>python manage.py runserver 8000</li>
</ol>
--------------------------------------<br />
Django Admin Panel:> 127.0.0.1/admin/ ::: #login required!
<br />
Custom Dashboard(admin panel):> 127.0.0.1/accounts/dashboard/ ::: #login required!
<br />
--------------------------------------<br>
Enjoy ❤️😍
