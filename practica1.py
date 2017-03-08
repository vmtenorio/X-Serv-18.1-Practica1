#/usr/bin/python3

import webapp
import csv

class shorten(webapp.webApp):
    def __init__(self, hostname, port):
        self.urlDict, self.writer = self.initDic()
        self.counter = 0
        webapp.webApp.__init__(self, hostname, port)

    def initDic(self):
        f = open('dict.csv', 'r')
        reader = csv.reader(f)
        urlDict = {}
        for row in reader:
            urlDict[row[0]] = row[1]
        f.close()
        fw = open('dict.csv', 'a')
        writer = csv.writer(fw)
        return (urlDict, writer)

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return request.split()

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        print(parsedRequest)
        if parsedRequest[1] == "/":
            if parsedRequest[0] == "GET":
                return ("200 OK", "<html><body><form method='POST'>" +
                                    "<input type='text' name='url'>" +
                                    "<input type='submit' value='Shorten'></form></body></html>")
            elif parsedRequest[0] == "POST":
                for i in parsedRequest:
                    if i.startswith("url"):
                        url = i.split('=')[1]
                        break
                self.urlDict[url] = self.counter
                self.writer.writerow([url] + [str(self.counter)])
                self.counter += 1
                return ("200 OK", "<html><body><p>" + url + str(self.counter) + "</p></body></html>")


        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")


if __name__ == '__main__':
    testShorten = shorten('localhost', 1234)
