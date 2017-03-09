#/usr/bin/python3

import webapp
import csv

class shorten(webapp.webApp):
    def __init__(self, hostname, port):
        self.counter = 0
        self.urlDict, self.writer = self.initDic()
        webapp.webApp.__init__(self, hostname, port)

    def initDic(self):
        f = open('dict.csv', 'r')
        reader = csv.reader(f)
        urlDict = {}
        for row in reader:
            urlDict[row[0]] = row[1]
            self.counter += 1
        f.close()
        fw = open('dict.csv', 'a')
        writer = csv.writer(fw)
        return (urlDict, writer)

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return request.split()

    def findUrl(self, shortenUrl):
        for k, v in self.urlDict.items():
            if v == shortenUrl:
                return k
        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        if parsedRequest[1] == "/dict":
            print(self.urlDict)
            return ("200 OK", "<html><body><h1>It works!</h1></body></html>")
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
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                if url in self.urlDict.keys():
                    return ("200 OK", "<html><body><p>URL: <a href='" + url +
                                        "'>" + url + "</a></p>" +
                                        "<p>Shortened URL: <a href='" + url + "'>" +
                                        str(self.urlDict[url]) + "</a></p></body></html>")
                else:
                    self.urlDict[url] = self.counter
                    #self.writer.writerow([url] + [str(self.counter)])
                    self.counter += 1
                    return ("200 OK", "<html><body><p>URL: <a href='" + url +
                                        "'>" + url + "</a></p>" +
                                        "<p>Shortened URL: <a href='" + url + "'>" +
                                        str(self.counter) + "</a></p></body></html>")
        else:
            url = self.findUrl(parsedRequest[1][1:])
            if url == None:
                return ("404 Not Found", "<html><body><h1>We couldnt find your URL</h1></body></html>")
            else:
                return ("303 See Other", "<html><head><meta http-equiv='Refresh' " +
                        "content='5;url=" + url + "'></head>" +
                        "<body><p>Seras redireccionado en 5 segundos o si haces click " +
                        "<a href='" + url + "'>aqui</a></p></body></html>")



        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")


if __name__ == '__main__':
    testShorten = shorten('localhost', 1234)
