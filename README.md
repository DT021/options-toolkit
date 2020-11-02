**Latest update**: I have moved existing python codes to the "legacy_python" folder, as I am moving this project toward the nodejs / electron platform. This way, the app runs locally, and people can use test out this app by using their own market data provider.

# options-toolkit
Simple tools that assist options trading and education.
This project is under GNU GPL 3.0 license, in order to encourage learning, sharing, and collaboration.

# Background
I am neither a professional trader nor a professional programmer (please don't judge my code; I know it looks amateurish). I am developing this toolkit because:
- I am interested in learning more about options, and developing an app would be an effective way to learn and put my knowledge into practice.
- I would like to develop tools that suit the needs of my investment strategy, to complement, not in place of, other tools I am using (which is why this is project is a "toolkit" rather than a "solution." Also, building an app from the ground up is also more flexible and practical.)
- I would like to gain some programming skills so that I can develop apps that relate to my careers and other interests.
- I am interested in helping people around me learn investing, and i would like to figure out ways to make options more intuitive for people to learn (hence data visualization is an important aspect of this project.)
- I would like to use this opportunity to communicate with people, get to know who they are and what they want, and even make friends.

# Methodology
The purpose of building a toolkit is to explore specific cases where data visualization and investment strategy come together. There are plenty of apps available that present all the data on a screen, and there is no need for me to reinvent the wheel. Instead, I would like to create a collection of small, highly-purposed tools where data presentations are not only helpful to investors but also highly tailored to particular investment strategies. In other words, what data is presented on the screen in a given tool is highly determined by how the data will be used by the investors for a certain task within a broader strategy.

For example, if one is interested in put credit spreads, instead of displaying all the information available (all the greeks, all hypothetical P/Ls, etc.), this app will display exactly what one needs to make a specific decision, such as finding the most profitable spread divided by days to expiration. Other data secondary to this primary goal will be presented only when they are needed.

# Contribute
Any contribution is appreciated, whether it's coding, testing, or general suggestions/recommendations regarding investing strategies, data visualizations, backend/frontend packages, and UI/UX.

## Testing on your own device

This package runs locally and retrieves data via your own Market Data API. Right now, only TD Ameritrade is supported. The API key will be stored locally in cache and will not be used or upload anywhere other than downloading data from the data provider(s).

# Bugs & bug reports
This project is in the initial stage of development and will likely contain many bugs. Since the main objective of this project is education and experimentation, there is no need to worry about identifying and fixing every bug, unless the main functionalities of the app fail to work at all. If you have any concerns, please feel free to use the "Issues" feature on Github or contact me directly.

Please feel free to contact me at sam-at-hermeneuticlens-dot-com