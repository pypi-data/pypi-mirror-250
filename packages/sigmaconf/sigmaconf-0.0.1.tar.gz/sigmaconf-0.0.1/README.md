# *SigmaConf* - A Simple Configuration Library for Science 

The goal of this library is to provide config dict-like objects with the following features:

* *Easy nested access*, e.g. `cfg['a.b.c']` instead of `cfg['a']['b']['c']`
* *Immutability*. Implemented as functional datastructures, which prevents unwanted side effects
* *Composability* - Configs can be easily combined, smartly merging nested structures
