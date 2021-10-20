---
layout: article
title: 'Coding In a Team: My First Research Internship'
---
What’s the difference between completing coursework as an undergraduate in physics and working in a real research team? One might conceive of the task as more meaningful, as it contributes to current research, or discuss how the content is more difficult, extending beyond the normal undergraduate curriculum. However, most prominent for me was how tightly cooperative the work is.

As an undergraduate you are always isolated by the need for your work to be ‘individual’. Of course we collaborate with lab partners and demonstrators to collect data and discuss ideas, however, much of your work you must do alone and show to nobody until it is assessed.

## A Team of Varied Skill Sets

This summer I undertook an undergraduate research project with the space and atmospheric physics group at Imperial. I worked as part of a team developing an application for citizen scientists to listen to audified magnetic field data, the Heliophysics Audified: Resonances in Plasmas (HARP) project. Much of my work was programming based, as I built an application to perform data import, initial data processing and time stretching (slowing) of audio.

I was struck by how enjoyable it was to work in a team with varied and complementary skill sets. It’s very rewarding to see how people’s varied experience comes together to help tackle the problems at hand, as well as to feel that you have value to contribute through your own experience and skills.

The project granted me a sense of competence and creative challenge, pushing me to develop new skills over its course. Initially, I obtained practise in deconstructing papers in order to understand them in more detail, including recreating some of the analysis in an earlier publication by my supervisor. This came in useful later, in particular because it gave me an understanding of the coordinate systems the satellite data was presented in and how to transform between them. Later on the project pushed me to expand my knowledge of programming tools and techniques, as I deployed my first python package on github and setup documentation generation for it.

Observing the input provided by others during meetings also offered some opportunity to learn about various topics outside my experience, although I found that this knowledge was often shallow. It’s difficult to gain an appreciation of the underlying structure of ideas without focused individual study.

I got to learn from observing the various discussions about the design of the app, publication planning, beta testing and surveys, not to mention learning quite a bit about magnetosphere physics and sonification techniques. In turn, I contributed my knowledge as a programmer: optimising algorithms, writing code and providing input on the design of the application architecture.

Perhaps most usefully over the course of the internship I was exposed to the various considerations when planning the next steps on a scientific project. I particularly noted the experimental approach taken to developing the application and user experience, such as the selection of the sonification algorithm through surveys. This was a more thorough interrogation of the assumptions underlying the choice of algorithms than I had expected and I appreciate that my supervisor was much more willing to not rely on his own judgement in this regard than I would have considered.

Overall, the experience illustrated to me where I need to learn to justify my assumptions and arguments more thoroughly as well as the benefit of seeking feedback earlier. I felt that I could have more regularly looked for ways to present my code and plans for feedback. Towards the end of the project, I performed better it this area, as I communicated more with my supervisor regarding the development of figures. These illustrated the function of the different time stretching algorithms we were investigating.

## Clean Code

During the project, I attempted to apply some of the principles I was learning about from watching [Robert C. Martin’s talks on Clean Code](https://www.youtube.com/watch?v=7EmboKQH8lM). These take a rigorous approach to guaranteeing the quality of computer code, in particular to enabling easy further development of the code.

In particular, I found the concept of code documenting itself through its variable names and structure power. I was gratified by how much this improved my experience programming the project, making it faster to make changes, such as changing the data import methodology. I also practised building unit tests for various functionality, which gave me some insight into the scope needed for thorough testing as well as the power of tests to grant confidence that my code works.

This project was also my first experience using git and github, which makes me disappointed that I didn’t start using source control earlier on.

## Lessons for the future

Some parts of the programming conversation didn’t go as smoothly. In the project, there was a need to build a means of communication between the C# code used on the UI side and the python code used to process the data. However, there was never a chance for me to talk to the person constructing the C# code. I felt that this lead to some misdirected planning, such as considering the use of SVG files in order to transfer data between the two parts, as the researchers coordinating were unable to convey any technical discussion outside their experience.

This reinforced to me the utility of having direct communication between those programming different parts of an application.

## An Area to Pursue

This research experience also served to emphasise how enjoyable I find the task of software development, as well as the significant skill set and knowledge I have built up. It’s also made clearer to me that I should orient myself towards software and application development as part of my future career, while illuminating many of the skills I have left to learn in this domain.
