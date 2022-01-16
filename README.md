# QuantRiskHedging
 
The idea behind this project is to give you an insight into the day-to-day strategic decision-making
process one could expect working on as a junior trader in a hedge fund. The explicit goal of this
project is an investigation into quantitative risk hedging with sparse and corrupted data.

## 1.1 Background
When a hedge fund portfolio manager (PM) comes up with a new idea for a trade, usually the
quantities of interest to the PM will not be directly tradeable. For example, suppose we expect
Canadian energy stocks to outperform American energy stocks over the next year due to faster
rising Fed rates in comparison to Canadian rates. There’s no direct product for this trade; however,
maybe longing the ETF XEG.TO and shorting the ETF XLE could accomplish this directive.
However, in this particular example, notice that XEG.TO is denominated in CAD, whereas XLE
is denominated in USD. Therefore, creating a portfolio with just these two constituents inherently
exposes the PM to foreign exchange (FX) risk. One method to remove this FX risk is to enter into
an FX swap agreement. These sort of considerations are at the pinnacle of what hedge funds focus
on day-to-day: hedging away risk to better trade quantities of interest.
For this project, we’ll be looking at Canadian markets. There are several concepts for which it
is advisable to familiarize oneself with, the most important will be tail risk.

## 1.2 The Question
The question in this project is how to practically tail hedge a data-sparse
portfolio against its historical tail risk.
Explicitly, you will be given a dataset, portfolio.csv. This dataset is derived from more than
1000 underlying constituents with an overall long position in each of the following markets:

1. Canadian or US (CAD-hedged) equities,
2. Canadian or US (CAD-hedged) fixed-income,
3. Canadian REITs
4. Canadian utilities
5. Canadian commodities

The instruments you’ll have at your disposal to hedge against tail risk are all sufficiently liquid
TSX traded equities and ETFs, and futures. By sufficiently liquid, we mean that there exists a
moving intraday bid-ask spread. As for the futures to look at, please concentrate only on the
following 4 futures: SXF, BAX, CGF, and CGB. You will find several ETFs particularly useful; most
notably those which track indices like the VIX (HUV.TO) and commodities (HGU.TO, XGD.TO,
etc).
Let us call the universe of tradeable assets for the purposes of hedging tail risk Ω (Canadian
equities, ETFs, & futures). The question you are asked to solve is as follows:
Select exactly 2 assets, w1,w2 2 Ω and find 2 weights w1,w2 such that w1 + w2 + cash = 1,
w1,w2 ̸2 (􀀀.1, 0.1), (short selling is allowed - more on that later, but need at least 10% capital in
each) so that your portfolio, P = w1w1 + w2w2 will make at least 10x the losses of the provided
portfolio on all tail risk events, but during the rest of the year will produce as little daily loss as
possible. This problem necessitates the need for a statistical model to find w1,w2 and thereafter
choose w1,w2.
The most challenging component of this assignment is the additional statistical model you will
need to provide to account for the missing data.
If you decide to short-sell a stock however, we will impose the constraint that at the time of
the purchase you will also need to keep 10% of your short sell’s value in cash. So for example, if
have $100 to invest and you short sell $100 worth of stock A, then you’ll need to hold $10 in cash
reserve, and you’ll have to invest exactly $190 worth into the stock B of your choice.

## 1.3 Data
We will be only concerned with daily close data.
The portfolio.csv data is provided at the following link. There are 4 tail risk events in our
portfolio history (history is Jan 1 2018 - Oct 9 2018, tail event defined as returns being more than 3
standard deviations away from standard returns, all tail events are losses):
• Tail event 1: Feb 2, 2018
• Tail event 2: Feb 5, 2018
• Tail event 3: Feb 8, 2018
• Tail event 4: Mar 22, 2018
In [2]: port = pd.read_csv('portfolio.csv')
port.head()
Out[2]: date price
0 2018-01-02 1.000000
1 2018-01-03 1.007464
2 2018-01-04 1.004797
3 2018-01-05 1.008368
4 2018-01-08 1.013282
You may use any data source to obtain stock, ETF, or future prices. I however would recommend
using Yahoo Finance for stocks & ETFs, and TMXMoney for Futures.

## 1.4 Solution
Please refer to the deck (Presentation.pptx)