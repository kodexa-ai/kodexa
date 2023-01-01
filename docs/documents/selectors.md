---
title: Selectors
---

Part of the core of the Kodexa platform is the ability to use selectors to find content within our document structure.

A selector works in a similar way to a CSS selector or an XPath. It allows you to build a query that can be executed on
an instance of a document.

For example if you wanted find all content nodes with the value “Name” you can do:

```python
document.select('//*[contentRegex("Name")]')
```

This would return an iterator of the content nodes (see
the [What is a Kodexa Document?](https://docs.kodexa.com/introduction/documents/overview))

Selectors are a powerful way to work and offer a number of clever features, the syntax is broken into a few parts:

:include-image: img_4.png {title: "Selector Structure", fit: true}

# Axis & Node Type

The axis is used to define how we are going to navigate the tree structure to identify the node types we want to match.
Some basic examples are:

| //           | Root node and all children                                              |
|--------------|-------------------------------------------------------------------------|
| /            | Root node                                                               |
| .            | Current Node  (or root if from the document)                            |
| ./line/.     | All nodes of type line under the current node                           |
| parent::line | Any node in the parent structure of this node that is of node type line |

# Predicate

The predicate for the nodes selected with the axis and node type is in square brackets. It can be made up a functions,
attributes and operators to allow you to further filter the nodes that you want to select.

Functions can be used in the predicate, these are:

| contentRegex | Return true if a regular expression on the content of the node matches

regularExpression:  The regular expression to use
includeChildren: True if you want to include the children of this node for the expression (optional, default false)
|
| --- | --- |
| typeRegex | Return true if a regular expression on the node type name matches

regularExpression:  The regular expression to use |
| tagRegex | Return true a regular expression on the tag name matches

regularExpression:  The regular expression to use |
| hasTag | Return true if the tag has the given name

tagName:  The name of the tag |
| hasFeature | Return true if a feature on the node has a value matching the provided type and name

featureType:  The feature type
featureName: The name of the feature |
| hasFeatureValue | Return true if a feature on the node has a value matching the provided type, name and value

featureType:  The feature type
featureName: The name of the feature
featureValue: The value of the feature |
| content | Returns the content of the node |
| uuid | Returns the UUID of the node |
| node_type | Returns the node type of the node |
| index | Returns the index of the node |

Also we support operators to allow you to combine functions, these are:

| | | Union the results of two sides |
| --- | --- |
| = | Test that two sides are equal |
| != | Test that two sides are not equal |
| intersect | Return the intersection of the two sides |
| and | Boolean AND operation on the two sides |
| or | Boolean OR operation on the two sides |

# Pipelines

Another concept that is available in selectors is a “pipeline”.

This allows use to chain together a list of selectors, where the results of the first selector are passed into the next
selector. This can be a useful way to build more complex queries against document structures.

For example:

```python
// word
stream * [hasTag("ORG")]
stream * [hasTag("PERSON")]
```

In the example above we stream all nodes of type word and then filter those that have the tag ORG, then filter those
that have the tag PERSON.

# Examples

Below are some examples of how you can use selectors: