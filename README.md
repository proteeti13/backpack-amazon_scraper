# backpack-scraper
How long does it take for your program to scrape each product on avg? 
answer : Almost 3 seconds for my code. Note that I wasn't able to scrape the categories, similar products and dimensions.

What could be some possible ways to make it even faster?
answer: One of the main bottleneck is the blcoking/terminating nature. The request is obviously going to be timed out even if I use selenium/ handle every exception. I need to hide my IP in some way. 
 he scraper can be run faster by implementing multithreading/ multiprocessing.
 
 Did you get flagged as robot while scraping? answer: Yes, while initially fetching the soup, I was flagged as a robot and parsed the "enter captcha" markup. I had to send my header information while sending requests to resolve this matter. 

At most I could get 34 product details, then the request gets timed out.
