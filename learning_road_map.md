

Async tasks:
	1.	How to update properties in migration
	2.	Concept of subquery (filter only those posts for which all the media items have been uploaded)
	3.	send mail (using google)
	4.	celery
	5.	rabbit mq
	6.	how to get graphical representation of all models in Django project

Swagger:
	1. Added swagger
	2. Capability to execute apis from browser itself
	3. add descriptions and parameters to documentation

Debugger for Celery:
	1. Create a new configration in launch.json for Celery
	2. run that configuration independently in a terminal

Micoroservices:

	1. So created a transcript web service 
	2. this webservice receives the url of a video, download it use google speech to text to generate the transcript
	3. One thing was observed that celery was processing only the alternate tasks
	4. So Dedicated queue was used 
