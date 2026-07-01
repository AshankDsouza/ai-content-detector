I want to build a very simple frontend. 

Technical specification:
Lets use html, vanilla javascript and css. 

Features:

1. A text box to input the text. 
2. A short description of what the website does. 

For now, lets go with:

Using a combination of digital trace detection and differences between stylometric patterns of AI generated content verses stylometric patterns of human generated content we are able to make very accurate assesments of text being AI generated or not. 

3. A credit line. Something like
©2026 by Ashank Dsouza. All rights reserved.

4. The verify button should be disabled until the text box has content with minumum characters. The verify button should send an API request and it should autogenerate the creator_id. A warning should be displayed if this condition is not met. Make sure there is an event listenor that picks up if the content has been edited or not and updates the disabling or enabling of the verify button accordingly. 

5. Make sure there is no CORs error. Lets use the correct fix this time if possible. We are accessing it via https://ai-generated-text.tech/ . Maybe we can try hosting the backend on https://ai-generated-text.tech/api ? I believe we will need to change the cloudfare configuration?