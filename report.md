# Report

## Question 1

Unfortunately, I was unable to get my python script to work errorlessly with the Mosquitto broker. My results would work sometimes, and fail silently othertimes.
I was therefore unable to run a suite of all 180 tests, because it would begin working for a little while with different QOS/delay/instance combinations,
but then silently fail on a random test (there was no pattern that I could find). I believe it is due to limitations with the Mosquitto broker and issues
with my python script's thread-based implementation. Other students reported similar problems, (see Nathan Woodburn's comment in Ed [here](https://edstem.org/au/courses/16155/discussion/1979794)).
All in all, I ran out of time to resolve this issue properly and so my results for question 1 will have to be this: 
a single Mosquitto broker (at least with the default configuration) does not appear to be able to handle several clients publishing at once with <5ms delays.
In my tests while debugging, when the delay was something more reasonable, even 50ms, the broker had no problems and I did not experience any crashes.
The aim of this assignment was to stress-test an MQTT broker, and in that sense I think I was successful. Like Nathan Woodburn and Logan De Groot, we found that
a single Mosquitto broker is not sophisticated enough to handle, robustly and repeatedly, multiple client connections with delays <5ms. 

If I had more time, I would like to have tested my current python program against a more sophisticated, production-grade MQTT broker to see how Mosquitto compares.

## Question 2



## Question 3

### Performance Challenges

As my tests showed (and other students replicated) even a popular, well-known MQTT broker struggles to handle 5 clients publishing with less than 5ms delay.
It is therefore not hard to imagine that an MQTT network with millions of sensors and thousands of subscribers would face considerable performance challenges.
In particular, many parts of the end-to-end system would come under strain:
- Network bandwidth - the large volume of messages from such a large network could easily overwhelm a network connection's bandwidth, 
particularly such as in our case, the sensors are transmitting with high-frequency. This would lead to congestion and increased latency.
- Broker resources - the MQTT broker needs to process and manage connections for all clients. With such a high volume of messages, the CPU and memory requires
could be substantial, meaning there could be bottlenecks if the system is not adequately provisioned.
- Buffer overflow - if the broker cannot process incoming messages quickly enough, they get queued in buffers. If the broker is not ultimately able to keep up,
this could lead to message losses or delays due to buffer overflows.
- Router performance - even if the broker is able to cope with scale, fail may result due to the intermediate devices such as routers.
The increased traffic must pass through a router to get to the broker, and if that router is not capable of dealing with this load, it could result
in dropped packets and thus message loss.


### QOS Considerations
In theory, MQTT is designed with different levels of service reliability depending on the need. The highlest level, QOS 2, ensures a message is delivered exactly
once at the cost of extra networking and computational resources. On the other hand, QOS 0 fires off messages without regard to whether they were received or not.
In theory, you would expect reducing the QOS to level 0 would help alleviate some of the resourcing concerns related to scale that we discussed above.
However, I believe this would depend on where the bottleneck is occuring. In my local tests, I found that with more publishers and a higher QOS,
there was significantly less messages than otherwise. If the bottleneck was a network-related one (as opposed to a broker CPU/memory issue), then
the reduced number of messages could potentially improve performance. Conversely, at a lower QOS, a publisher could spam the network with
a much faster rate of messages, potentially congesting the network or router leading to eventual message losses and system failure.
