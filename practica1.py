#/usr/bin/python3

import webapp
import csv

class shorten(webapp.webApp):
    def __init__(self, hostname, port):
        self.counter = 0
        self.urlString = ""
        self.urlDict, self.writer = self.initDic()
        webapp.webApp.__init__(self, hostname, port)

    def initDic(self):
        try:
            f = open('dict.csv', 'r')
        except FileNotFoundError:
            f = open('dict.csv', 'w+')
        reader = csv.reader(f)
        urlDict = {}
        for row in reader:
            urlDict[row[0]] = int(row[1])
            self.urlString += "<p><a href='" + row[0] + "'>" + row[0] + "</a>: <a href='" + row[1] + "'>" + row[1] + "</a></p>"
            self.counter += 1
        f.close()
        fw = open('dict.csv', 'a')
        writer = csv.writer(fw)
        return (urlDict, writer)

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        request = request.replace("%2F",'/').replace("%3A", ':')
        return request.split()

    def findUrl(self, shortenUrl):
        for k, v in self.urlDict.items():
            if str(v) == shortenUrl:
                return k
        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        if len(parsedRequest) == 0:
            return ("404 Not Found", "<html><body><h1>Some error ocurred</h1></body></html>")
        if parsedRequest[1] == "/":
            if parsedRequest[0] == "GET":
                return ("200 OK", "<html><body><form method='POST'>" +
                                    "<input type='text' name='url'>" +
                                    "<input type='submit' value='Shorten'></form>" +
                                    "<h1>URL disponibles: </h1>" +
                                    self.urlString + "</body></html>")
            elif parsedRequest[0] == "POST":
                url = None
                for i in parsedRequest:
                    if i.startswith("url"):
                        url = i.split('=')[1]
                        break
                if url == None:
                    return ("404 Not Found", "<html><body><h1>We couldnt find your URL</h1></body></html>")
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                if url in self.urlDict.keys():
                    return ("200 OK", "<html><body><p>URL: <a href='" + url +
                                        "'>" + url + "</a></p>" +
                                        "<p>Shortened URL: <a href='" + str(self.urlDict[url]) + "'>" +
                                        str(self.urlDict[url]) + "</a></p></body></html>")
                else:
                    self.counter += 1
                    self.urlDict[url] = self.counter
                    self.urlString += "<p><a href='" + url + "'>" + url + "</a>: <a href='" + str(self.counter) + "'>" + str(self.counter) + "</a></p>"
                    self.writer.writerow([url] + [str(self.counter)])
                    return ("200 OK", "<html><body><p>URL: <a href='" + url +
                                        "'>" + url + "</a></p>" +
                                        "<p>Shortened URL: <a href='" + str(self.counter) + "'>" +
                                        str(self.counter) + "</a></p></body></html>")
        else:
            url = self.findUrl(parsedRequest[1][1:])
            if url == None:
                return ("404 Not Found", "<html><body><h1>We couldnt find your URL</h1></body></html>")
            else:
                return ("303 See Other", "<html><head><meta http-equiv='Refresh' " +
                        "content='2;url=" + url + "'></head>" +
                        "<body><p>Seras redireccionado a " + url + " en 2 segundos o si haces click " +
                        "<a href='" + url + "'>aqui</a></p></body></html>")


if __name__ == '__main__':
    testShorten = shorten('localhost', 1234)
