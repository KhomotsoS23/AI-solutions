systemPrompt = "Synthesize multiple meeting transcript chunk summaries into a comprehensive meeting summary of 1800-2000 characters. Focus on key themes, decisions, and action items across the entire meeting. Present a coherent narrative of the meeting's progression and outcomes."
userPrompt = "Create a final meeting summary from the provided chunk summaries. Structure your summary as follows: 1) Brief meeting context, 2) Main topics discussed (chronological order), 3) Key decisions made, 4) Action items (with assignees and deadlines), 5) Unresolved issues, 6) Brief conclusion. Resolve any contradictions by favoring the most recent information. Avoid repetition and focus on the meeting's overall narrative and outcomes."
exampleInputs = ["""
0:04: Good morning, everyone. 
 0:06: Today is Monday. 
 0:06: We are going to continue on with phase two. 
 0:11: We are nearing the end. 
 16:04: But Sharon, did you wanna answer the, you wanna circle back on those questions from Wednesday that Cynthia had? 
 16:12: Yeah, absolutely. 
 16:13: I can do that. 
 16:14: Ok, before we do that. 
 16:15: Sorry, I didn't, I didn't mind transition. 
 16:16: Did anybody else have any other points to bring up before we change into that? 
 16:22: No, I, I stopped sharing. 
 16:25: Ok. 
 16:27: It would you share? 
 16:28: Ok, thank you, Jon. 
 16:30: So from our last call on Wednesday, there are two questions that I don't think we really were able to answer in, you know, completely. 
 16:42: So I wanted to circle back to those and the first one was around reference data sets and if you're able to connect them to one another. 
 16:53: And so I was looking into that a bit more, let me share my screen. 
 17:06: So this is in the documentation for cloud pack for data. 
 17:10: And so I haven't tested this with like the mock data we have with like the reference data mapping. 
 17:18: But what I had found is this page in the documentation that talks about being able to establish hierarchies and relationships for your reference data. 
 17:29: So like the example here, you can see, I don't know if I can zoom in but oh, there you go. 
 17:36: You have like a country table, a code table and then a currency code table and so you can relate tables back to each other. 
 17:43: So you're able in cloud pack for excuse me tongue time and cloud pack for data set, those relationships between the reference data. 
 17:54: And I believe that's what the question was if I understood it correctly from Wednesday. 
 17:59: , and so you are able to do that. 
 18:02: And if this is answering that question, I can share this back with the recording,, from today. 
 18:10: Hi Sharon. 
 18:11: , I think it answers the question and I was also,, wondering, you know, between our tables and the reference table, which I believe it can do. 
 18:21: , but I think the one issue that we ran into was the ability to make some of those relationships when we couldn't get into the refinery because I, I believe that, you know, setting some of those keys within the tables were dependent on that functionality. 
 18:43: So I think we should be good going forward once we have that ability. 
 18:48: OK. 
 18:49: So I guess once you're, you know, once we have these blockers solved, if you could give this another look and just see, you know, if you have success with this and if not, we can, you know, circle back to helping you through any problems around reference data. 
 19:06: Does that work? 
 19:07: Sounds good. 
 19:08: Thank you very much Sharon, of course. 
 19:12: And then the second question that I had written down was around setting them in, in max values for your data classes. 
 19:27: So I believe the question was whether you should set the min max value beforehand, if you're trying to account for like null values in your enrichment. 
 19:42: And so through a little bit of digging, I did test it out and there is, I guess I should go to the enrichment first in your data quality checks. 
 24:49: I mean, yeah, you guys, we're, we're definitely feeling like we're on a journey with OMH right, starting to, you know, better manage data data quality. 
 25:01: But you know, we as far as adding, you know, additional capabilities, you know, like match 360 or AI functionality to govern and manage, you know, A I you know, that's something we can definitely share more, you know, brief you guys on so you can understand what it's all about and, and plan on, you know, applying it or, you know, whatever decisions you come to, you know, we happy to, to do that. 
 25:36: Thank you. 
 25:36: , now, but just to pick up on that,, a little bit. 
 25:41: Do, do you wanna schedule some time with, with the, you know, the, the larger group or a smaller group? 
 25:47: I, I'm curious what, what you want to, you know, what you kinda wanna,, you know, it, I, I think that will be, that will be decision from the O Mh Amy can take this decision. 
 26:02: But, you know, I, I, I just want to curious about those are the advanced features you have, you know, why don't do the group should understand those concepts and services for the picture of thought, data quality analysis, you know, those are the A I related. 
 26:22: So everything is going to the, to the A I? 
 26:25: Right, right now. 
 26:27: So why don't you use that one? 
 26:29: You know, those services? 
 26:32: Music to our ears. 
 26:34: Yep. 
 26:34: Absolutely. 
 26:41: No, but I'll, I'll, I'll send you,, a, a note, you know, after this call just to, to see if you know how we'd wanna do that. 
 26:49: You know, and,, pick up on that, on that,, thread there. 
 26:52: Ok, thank you. 
 26:54: Yeah. 
 26:54: Yeah, you got it. 
 26:57: Should I, Andy, hey,, Brian and Tom and I guess,, yeah, it's Brian. 
 27:04: Tom Cynthia. 
 27:05: Are you, are you guys free Friday after three o'clock? 
 27:09: I was able just to pull up people's calendar. 
 27:12: , looks like we all are or available Friday, Friday after 33 is fine for me. 

                 """
]
exampleOutputs = ["""
Data Quality And Analysis Project Call

Context: IBM and New York State OMH team met to continue progression on phase 2 of Data Quality project

Key points:
Project is currently in phase 2 of development
IBM answered questions from last call regarding reference data and setting min/max values for data classes
Client is interested in learning more about Master Data Management and Match 360

Action items:
IBM to provide some more information on Mach 360 and MDM soilutions to OMH team

Next Steps:
Follow up meeting on friday to discuss requested services information for Match 360 and MDM

Conclusion: The Data Quality project with OMH is currently in phase 2. This call focused on answering some questions the client had asked in the previous meeting. Client is also interested in seeing MAtch 360 and Master Data Management (MDM) services, which a follow up call on Friday was confirmed to discuss further.
"""
]