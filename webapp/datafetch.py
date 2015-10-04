from google.appengine.ext import ndb

import webapp2

class Currency(ndb.Model):
	value = ndb.StringProperty()
	
MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/fetch" method="post">
      <div><input type="text" name="currency"></div>
      <div><input type="submit" value="Fetch currency data"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Getvalue(webapp2.RequestHandler):
    def post(self):
		curr = self.request.get('currency')
		key = ndb.Key(Currency, curr)
		self.response.write('<html><body>Currency values:<pre>')
		vals = Currency.query(ancestor=key)
		#self.response.write(vals)
		for ent in vals:
			self.response.write('<br>')
			self.response.write(ent.value)
			self.response.write('<br>')
		self.response.write('</pre></body></html>')
		
app = webapp2.WSGIApplication([
	('/curr', MainPage),
	('/fetch', Getvalue),
], debug=True)