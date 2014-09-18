#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PyvotalTrackerBroker - bitbucket broker to use with pyvotaltracker.com"""

#Copyright 2010 Paul Okopny. All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, arepermitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY PAUL OKOPNY ``AS IS'' AND ANY EXPRESS OR
#IMPLIEDWARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#OF MERCHANTABILITY ANDFITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#IN NO EVENT SHALL PAUL OKOPNY ORCONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, ORCONSEQUENTIAL DAMAGES (INCLUDING,
#BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS ORSERVICES; LOSS OF USE,
#DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ONANY THEORY
#OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDINGNEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IFADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are
#those of theauthors and should not be interpreted as representing official
#policies, either expressedor implied, of Paul Okopny.

import urllib
import urllib2
import json
# from brokers import BaseBroker

class PivotalTracker():

    def __init__(self, token):
        self.token = token

### for testing:
###class PivotalTracker(object):
    """\
    Post-commit broker for tracker: pivotaltracker.com

    Your commit message should have square brackets containing a hash mark followed by the story ID.
    If a story was not already started (it was in the "not started" state),
    a commit message will automatically start it.
    To automatically finish a story by using a commit message,
    include "fixed", "completed" or "finished" in the square brackets in addition to the story ID.

    For more info visit https://www.pivotaltracker.com/help/api?version=v3#scm_post_commit
    """
    def handle(self, payload):
        """\
        Commit message syntax:

            Commit: Username
              54321

              [#12345677 #12345678] Alpha-version is done. Going to beta.

        For more info visit https://www.pivotaltracker.com/help/api?version=v3#scm_post_commit
        """
        url = "http://www.pivotaltracker.com/services/v3/source_commits/"

        token = self.token #payload['service']['token']

        headers = {'X-TrackerToken': token, 'Content-type': 'application/xml' }

        print payload
        print type(payload)

        payload = json.loads(payload)
        print payload
        print type(payload)

        for commit in payload['commits']:

            #Ok. This part a little bit ugly. Composing URL to changeset.

##            chset_url = payload['repository']['website'] \
##                + payload['repository']['absolute_url'][1:] \
##                + 'changeset/' + commit['node']

            #Paul's code for generation changeset-URL

            commit['url'] = payload['repository']['website'] \
                + payload['repository']['absolute_url'][1:] \
                + 'changeset/' + commit['node']


            #create TinyURL
##            res = urllib2.urlopen('http://tinyurl.com/api-create.php?url=' \
##              + chset_url)
##            commit['url'] = res.read()



            #Compiling all of it into xml to send to pivotaltracker
            xml = """<source_commit><message>%(message)s</message>\
<author>%(author)s</author><commit_id>%(node)s</commit_id>\
<url>%(url)s</url></source_commit>""" % commit

            # xml = urllib.quote_plus(xml)

            #debug output
##            print chset_url
##            print commit['url']
##            print xml

            req = urllib2.Request(url, xml, headers )
            f = urllib2.urlopen(req)

            print f.read()


#Testing. Payload data taken from bitbucket.org help and modified a little bit.
#Uncomment this code to test it in local. Do not forget about BaseBroker class
"""
if __name__ == "__main__":
    token = "some token taken from pivotaltracker"

    payload = {'broker': u'PivotBroker',
                 'commits': [{ 'author': 'myname',
                        'files': [{'file': u'media/css/layout.css',
                                    'type': u'modified'},
                                    {'file': u'apps/bb/views.py',
                                    'type': u'modified'},
                                    {'file': u'templates/issues/issue.html',
                                        'type': u'modified'}],
                               'message': '[#3530757 finished] now it is ok',
                               'node': u'changeset!',
                               'revision': 123,
                               'size': 654}],
                 'repository': { 'absolute_url': u'/myname/myproject/',
                                 'name': u'bitbucket',
                                 'owner': u'myname',
                                 'slug': u'bitbucket',
                                 'website': u'http://bitbucket.org/'},
                 'service': {'token': token }}

    p = PivotalTracker()
    p.handle(payload)
"""

