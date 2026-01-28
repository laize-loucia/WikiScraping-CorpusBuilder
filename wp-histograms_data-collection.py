# configuration : provide the titles and languages of the pages you want to analyse
#pages = [('Artificial intelligence', 'en'), ('Intelligence artificielle', 'fr'), ('Machine learning', 'en'), ('Apprentissage automatique', 'fr'), ('Deep learning', 'en'), ('Apprentissage profond', 'fr'), ('Artificial neural network', 'en'), ('Réseau de neurones artificiels', 'fr')]


import requests, time


#liste de tuples = mini-listes
pages = [('Blockchain', 'en'), ('Blockchain.com', 'en'), ('Terra (blockchain)', 'en'), ('Solana (blockchain platform)', 'en'), ('Fork (blockchain)', 'en'), ('Privacy and blockchain', 'en'), ('Chainlink (blockchain)', 'en'), ('List of blockchains', 'en'), ('Polygon (blockchain)', 'en'), ('Blockchain game', 'en'), ('Blockchain Capital', 'en'), ('Stacks blockchain', 'en'), ('Cardano (blockchain platform)', 'en'), ('Blockchain oracle', 'en'), ('Avalanche (blockchain platform)', 'en'), ('Blockchain as a service', 'en'), ('Blockchain analysis', 'en'), ('Long Blockchain Corp', 'en'), ('Blockchain Chicken Farm', 'en'), ('Blockchain-based database', 'en'), ('Blockchain Global', 'en'), ('Blockchain Labs', 'en'), ('List of people in blockchain technology', 'en'), ('Congressional Blockchain Caucus', 'en'), ('ICON (blockchain platform)', 'en'), ('Proof of identity (blockchain consensus)', 'en'), ('Non-fungible token', 'en'), ('Cryptocurrency', 'en'), ('Bitcoin', 'en'), ('Bitcoin protocol', 'en'), ('Everipedia', 'en'), ('Solidity', 'en'), ('The Open Network', 'en'), ('Trusted timestamping', 'en'), ('Hardware security module', 'en'), ('The Sandbox (company)', 'en'), ('History of bitcoin', 'en'), ('Decentralized web', 'en'), ('Justin Sun', 'en'), ('Trade finance technology', 'en'), ('GITEX', 'en'), ('Diem (digital currency)', 'en'), ('Stoned (computer virus)', 'en'), ('MC Lars discography', 'en'), ('Cryptocurrency and crime', 'en'), ('Microsoft Azure', 'en'), ('Kickstarter', 'en'), ('Do Kwon', 'en'), ('Kerala University of Digital Sciences, Innovation and Technology', 'en'), ('Distributed ledger technology law', 'en'), ('Politics and technology', 'en'), ('Aggelos Kiayias', 'en'), ('UBS', 'en'), ('List of software bugs', 'en'), ('Bruce Schneier', 'en'), ('X-Road', 'en'), ('Wan Kuok-koi', 'en'), ('Garbage Pail Kids', 'en'), ('William Entriken', 'en'), ('Key ceremony', 'en'), ('List of Internet top-level domains', 'en'), ('Chea Serey', 'en'), ('Financial audit', 'en'), ('Dish Network', 'en'), ('Jason Fernandes', 'en'), ('Governance', 'en'), ('Virgil Griffith', 'en'), ('Marine technology', 'en'), ('Generative art', 'en'), ('List of cyberattacks', 'en'), ('Michael Jones (entrepreneur)', 'en'), ('Local differential privacy', 'en'), ('Sumitomo Mitsui Banking Corporation', 'en'), ('Ayia Napa', 'en'), ('Zero-knowledge proof', 'en'), ('Digital art', 'en'), ('Regulation of algorithms', 'en'), ('Hash chain', 'en'), ('Data sanitization', 'en'), ('Non-interactive zero-knowledge proof', 'en'), ('As a service', 'en'), ('Network effect', 'en'), ('History of video games', 'en'), ('This Place (agency)', 'en'), ('Bill Buchanan (computer scientist)', 'en'), ('Daniel Harple', 'en'), ('Victor Acevedo', 'en'), ('Nancy Baker Cahill', 'en'), ('Pavel Vrublevsky', 'en'), ('Justin Waldron', 'en'), ('Iyasile Naa', 'en'), ('Peter Chen', 'en'), ('Legerwood, Tasmania', 'en'), ('Hernando de Soto (economist)', 'en'), ('List of View Askewniverse characters', 'en'), ('Audit technology', 'en'), ('Satish Babu', 'en'), ('Frankie Bash', 'en'), ('Jeff Pulver', 'en'), ('List of Atari SA subsidiaries', 'en'), ('Visible Embryo Project', 'en'), ('Bangladesh Computer Council', 'en'), ('Drecom', 'en'), ('Redbank Power Station', 'en')]


today = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.localtime())
today_out = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

print('Data collection may take a few minutes, particularly if the articles have been heavily edited or if you are collecting a large number of articles. Have a cup of tea.')

# for each page
for page in pages :
	print('Collecting for ' + str(page))
	
	# we initialize a liste of revision timestamps
	revisions = []

	# we create a first API request
	# see documentation : https://www.mediawiki.org/wiki/API:Revisions
	# here we collect revisions from the oldest to the newest, by batches of 100
	url = 'https://' + page[1] + '.wikipedia.org/w/api.php?action=query&prop=revisions&titles=' + page[0] + '&rvlimit=100&rvprop=timestamp|ids&rvdir=newer&rvend=' + today + '&format=json'
	
	# for more infos on the edits and users :
	# https://fr.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Intelligence%20artificielle&rvlimit=100&rvprop=timestamp|ids|size|flags|user&rvdir=newer&rvend=2022-10-28T19:42:50Z&format=json
	
	# looping to manage the continuation requests
	while len(url) > 0 :
		try:
			req = requests.get(url,timeout=30)
			req.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)
		time.sleep(1)
		
		# adding the resulting timestamps to the list
		data =  req.json()
		pageid = list(data['query']['pages'].keys())[0]
		for revision in data['query']['pages'][pageid]['revisions'] :
			revisions.append(revision['timestamp'])
		
		# if there is more than 100 revision, we prepare a continuation request
		if 'continue' in data :
			url = 'https://' + page[1] + '.wikipedia.org/w/api.php?action=query&prop=revisions&titles=' + page[0] + '&rvlimit=100&rvprop=timestamp|ids&rvdir=newer&rvend=' + today + '&format=json&rvcontinue=' + data['continue']['rvcontinue']
		# else, we make it stop
		else :
			url= ''
	
	# we save all the revision timestamps in a CSV file (one timestamp per line)
	print('\t' + str(len(revisions)) + ' revisions found')
	out = open(today_out + '_' + page[1] + '_' + page[0] + '.csv', 'w', encoding='utf-8')
	for revision in revisions :
		out.write(revision + '\n')
	out.close()

	
