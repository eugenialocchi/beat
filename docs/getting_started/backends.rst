Sampling Backends
-----------------

Currently, there are two *backends* implemented that allow to select the format in which the sampling results are stored to the disc.

 + csv- comma separated value: This format is good for getting started, debugging and to inspect the content and form of sampling results that are written to disc. Any text editor can easily open these files and the user can check if sampled values are reasonable. However, resulting disc space needed for storing the samples is large and the performance of reading and writing is low.
 + bin- binary: This format is good once the user knows what is going on and when performance matters for longer sophisticated model runs. Speed of reading and writing is ca. 100 times faster than with the *csv* format and required disc space is less. However, accessing the content of the files is more complicated through the BEAT-API and is not human readable.

The first lines of the *SamplerConfigs*::

  sampler_config: !beat.SamplerConfig
    name: SMC
    backend: bin  # could be also "csv"
    progressbar: true
    buffer_size: 1000
    buffer_thinning: 50

Two parameters determine the behavior of the sampling backends.

*buffer_size* determines the number of samples after which results are written to disc.

*buffer_thinning* e.g. with 50 here, every 50th sample is going to be written to files. This is useful to significantly reduce the amount of disc space that is needed to store the samples obtained with the *SMC* sampler. Especially, for setups with hundreds of random variables and thousands of chains this can make a difference of hundreds of giga-bytes. For the intermediate PDFs that are being sampled by the *SMC* only the last samples of the stage are needed to transition into the next stage. Thus, it is ok to throw away the rest.
