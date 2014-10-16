========
Introduction
========

Basics of data storage
==============

A good data storage system is an important component of any financial system. 

Data could be classified on the basis of density and sparsity. A dataset is called dense when almost all fields are filled up for all rows.

DataFrame - rows and columns

sparse data - a lot of rows but only few columns
dense data - a lot of rows with all columns filled up

sparse data could be represented as key value pairs and dense data as arrays.

HDF5 is the specified format

Basically two types of data types are used - arrays and key/value pairs.
Arrays are represented by csv files and key/value pairs as json files. Both the formats must be interchangeable
