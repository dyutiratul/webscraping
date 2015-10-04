from google.appengine.ext import ndb

import lxml.etree
import webapp2

class Currency(ndb.Model):
	value = ndb.StringProperty()
	
class Parsefile(webapp2.RequestHandler):
	def get(self):
		e = lxml.etree.parse('forexCalendarTomorrow.xml')
		self.response.write('<html><body>Storing values<pre>')
		for atype in e.xpath('//currency'):
			subfields = atype.getchildren()
			curr = Currency()
			for subfield in subfields:
				currkey = ndb.Key(Currency, subfield.tag)
				curr = Currency(value=subfield.text, parent=currkey)
				curr.put()
		self.response.write('Data saved')
		self.response.write('<br>')
		self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/save', Parsefile),
], debug=True)