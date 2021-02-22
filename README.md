# Cybereason - Oracle Cloud Guard integration

## Introduction

This document outlines the steps required to set up and use the Cybereason - Oracle Cloud Guard integration. When a problem is detected (e.g. an instance has a public IP) by Cloud Guard, a separate investigation is launched into the Cybereason Console. If Cybereason flags the activity as suspicious, then the integration can isolate the machine and/or send notifications to a specified Topic.

## Setup Notes
### Pre-requisites
Before starting, please ensure that you have the following:
1. An account with a Cybereason web console with API access. The web console is typically accessible at a URL like `https://<tenant>.cybereason.net`.
1. An account with Oracle Cloud with administrator privileges.
1. Experience with using Terraform templates.

Once you have your pre-requisites sorted, use the following steps to set up the integration. Broadly, this is done in two steps:
1. Set up the responder funtion image as described in [Function Image Setup](installation-guide/FUNCTION.md)
1. Set up the function and associated resources as described in [Terraform Setup](installation-guide/TERRAFORM.md)
1. Set up logging for the function and events service as described in [Logging](installation-guide/LOGGING.md)

## How to Test
This repository contains a few sample Cloud Guard payloads that you can use to test the functions. The samples are provided as JSON files in the `sample-payloads/` folder. These are given for reference only - you will most probably have to generate your own payloads from the configuration (compartments, instances, etc) that you have in your tenancy.

Once you have a payload for your tenancy, you can test the function by typing
```
cat <payload file> | fn invoke <Application> <Function>
```
Where `<payload file>` is a JSON file with the Cloud Guard payload, `<Application>` is the name of your Cybereason Responder application, and `<Function>` is the name of your Cybereason Responder function.
