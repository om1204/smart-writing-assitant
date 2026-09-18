export const samples = [
  // Test 1: SAR / Earth Observation — Full Pipeline
  'i want to understand that how the earthmind architeture is woking and how it process the SAR images because the raw satelite data is very huge and it have many differnt informations. the model first take the image and then it compress them into small tokens however i am not sure why this compression is needed and what information is lost during this step. the researcher said that the encoder extract important visual features but they does not clearly explain which features are kept. therefore the system can process the image more efficently but it maybe loose some spatial details. when i read the paper i was confused because it say that the model uses a transformer after the compression, but the transformer only see the compressed representation and not the original image.',
  
  // Test 2: University Email
  'sir i am writing this mail because i have a problem regarding the assignment which was suppose to be submitted yesterday. i was working on the NLP project and my laptop suddenly stop working while i was running the code, because of this i could not complete the final testing and the result was not generated. i tried to fix it but it take almost four hours and after that the system was still showing errors. therefore i am requesting you to please give me some extra time for submitting the assignment. i know that the deadline was already given and i should have completed it before, however the problem was unexpected and i have already completed most of the work.',
  
  // Test 3: Bank WSD
  'yesterday i went to the bank near the river because i needed to deposit some money. while i was walking there my friend called me and asked if i had seen the new bank that was opened beside the river bank. at first i thought he was talking about the financial bank but he was actually talking about the bank of the river where a small construction team was working. they were putting some equipment there because the water level had increased after the rain.',
  
  // Test 4: Coreference Nightmare
  'rahul told arjun that he should send the report to the professor because he had already finished it. when he reached the lab he gave it to him but he was not there so he left it on his desk. later the professor called rahul and said that the report was missing some important information. rahul told him that arjun had prepared the final version but arjun said that he only checked the calculations and rahul had written the main part. however they both thought that the other person had submitted the report.',
  
  // Test 5: Climate Science
  'climate change is becoming more serious every year and scientist are collecting huge amount of data from satellites, weather stations and ocean sensors. this data help them understand how temperature, rainfall and sea level is changing across different regions. however the data is not always clean because some sensors stop working and some measurements contain errors. when researchers combine these sources they need to decide which values should be trusted and which should be removed. therefore data preprocessing is very important before a machine learning model is trained.',
  
  // Test 6: Bat WSD
  'the boy picked up the bat and went outside because he wanted to practice before the match. his father was sitting near the window and asked him why he was carrying a bat so early in the morning. the boy said that he needed to improve his swing because the last match was very difficult. while they were talking a bat suddenly flew across the garden and landed near the tree. his father laughed and said that there was another kind of bat in the garden too.',
  
  // Test 7: Software Engineering
  'the application was designed to process large documents but it was running very slow when the user upload more than fifty pages. initially the developer thought that the database was the problem but after checking the logs he found that the NLP model was processing every sentence multiple times. because of this the response time become very high and users started complaining that the application was hanging. therefore the developer changed the pipeline so that intermediate results were cached and reused whenever possible. however this solution introduced another problem because old results was sometimes returned even after the document was changed.',
  
  // Test 8: Machine Learning Assignment
  'machine learning is a part of artificial inteligence which allow computer to learn from data without explictly programming every rule. there are many type of machine learning like supervised unsupervised and reinforcement learning. in supervised learning the model get labeled data and it learn a mapping between input and output. for example if we give many images of cats and dogs then the model can learn to predict whether a new image is cat or dog. however if the training data is biased or have mistakes then the model can also learn those mistakes. this is why data quality is very important.',
  
  // Test 9: Full Stress Test
  'orignal: last week me and my friend was discussing about whether AI can really understand images or it just learn patterns from huge amount of data. he said that modern vision language models can process very complex images, however i was not fully agree with him because when the image contain very small objects the model sometimes give incorrect answers. then he showed me a satellite image and asked me what is visible in it. i said that there are some roads, buildings and maybe a small vehicle near the river. he told me that the vehicle was actually a boat but i could not see it clearly. because the resolution was low, it was difficult to identify the object and this made me think about how visual compression affects the information that a model receive. the researcher who wrote the paper said that the encoder first convert the image into a smaller representation and then the language model process it. however if important details are removed during compression then the language model cannot recover them later, even if it is very powerful. therefore i think a good vision language architecture should not only focus on reducing computation but should also preserve the information which is necessary for the final task.',
  
  // Test 10: Pragmatic Inference
  'the project meeting was scheduled at ten but nobody had prepared the presentation. the team leader entered the room and asked whether someone could share the latest slides with everyone. one member replied that the slides were on his laptop but his laptop was currently updating. the leader then asked if somebody could maybe send the file before the meeting started. another student said that he could do it but he needed access to the shared folder first. the leader looked at him and said that it would be great if someone could check the permissions. after a few minutes they realized that the folder was restricted to only two members of the team. therefore they changed the permissions and uploaded the presentation. however when they opened it they found that several diagrams were missing because the original file had not been saved correctly.'
]

export const sampleLabels = [
  'Test 1: SAR / Earth Observation',
  'Test 2: University Email',
  'Test 3: Bank WSD',
  'Test 4: Coreference Nightmare',
  'Test 5: Climate Science',
  'Test 6: Bat WSD',
  'Test 7: Software Engineering',
  'Test 8: Machine Learning',
  'Test 9: Full Stress Test',
  'Test 10: Pragmatic Inference'
]

export const stages = [
  ['spell', 'Stage 1: Spell Check'],
  ['syntax', 'Stage 2: Syntax & Parsing'],
  ['semantic', 'Stage 3: Semantics & WSD'],
  ['discourse', 'Stage 4: Discourse & Pragmatics'],
  ['full', 'Stage 5: Full Pipeline Overview']
]
