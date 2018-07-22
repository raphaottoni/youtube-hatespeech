from bs4 import BeautifulSoup
import urllib3
import csv

# Where the results will be saved
output_locaiton = "../../data/mediasbias.csv"

# Disable IsecureRequestWarnings beause we arent using certificates to query
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# base http address of mediabiasfackcheck 
media_bias_url = "mediabiasfactcheck.com"

# List of the political spectrum we will collect (those names must match the ones used in mediabiasfactcheck.com
spectrum = ["conspiracy", "left", "leftcenter", "center", "right-center", "right" ]

# Collect all the medias associated with each spectrum
medias_by_bias = {}

http = urllib3.PoolManager()

print("Collecting medias with "+ "/".join(spectrum) + " bias ...")
for bias in spectrum:
    request  = http.request('GET', media_bias_url + "/" + bias)
    soup = BeautifulSoup(request.data, 'html.parser')
    medias = soup.article.find_all("p")[1].find_all('a')
    get_medias = lambda medias: [media.getText().rstrip("\r\n").lower() for media in medias]
    medias = get_medias(medias)
    medias_by_bias[bias] = medias
print("Done!")


print("Writing csv file to " + output_locaiton)
# write csv with all medias name and the associated bias
with open(output_locaiton, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for bias, medias in medias_by_bias.items():
        for media in medias:
            if media != "": writer.writerow([media, bias])
print("Done!")
