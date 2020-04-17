# LibSRTP
[GitHub](https://github.com/cisco/libsrtp)

This package provides an implementation of the Secure Real-time Transport Protocol
 (SRTP), the Universal Security Transform (UST), and a supporting cryptographic 
 kernel. The SRTP API is documented in include/srtp.h, and the library is in 
 libsrtp2.a (after compilation).

This document describes libSRTP, the Open Source Secure RTP library from 
Cisco Systems, Inc. RTP is the Real-time Transport Protocol, an IETF standard 
for the transport of real-time data such as telephony, audio, and video, 
defined by RFC 3550. Secure RTP (SRTP) is an RTP profile for providing 
confidentiality to RTP data and authentication to the RTP header and payload. 
SRTP is an IETF Standard, defined in RFC 3711, and was developed in the 
IETF Audio/Video Transport (AVT) Working Group. This library supports 
all of the mandatory features of SRTP, but not all of the optional features. 
See the Supported Features section for more detailed information.

This document is also used to generate the documentation files in the /doc/ 
folder where a more detailed reference to the libSRTP API and related functions 
can be created (requires installing doxygen.). The reference material is created 
automatically from comments embedded in some of the C header files. 
The documentation is organized into modules in order to improve its clarity. 
These modules do not directly correspond to files. An underlying cryptographic 
kernel provides much of the basic functionality of libSRTP but is mostly 
undocumented because it does its work behind the scenes.

