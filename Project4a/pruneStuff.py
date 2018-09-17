# if len(examples) == 0:
#     return LeafNode(defaultLabel)
#
# same = True
# firstEx = examples[0][className]
# for ex in examples:
#     if ex[className] != firstEx:
#         same = False
#         break
# if same:
#     return LeafNode(firstEx)
#
# if len(remainingAttributes) == 0:
#     return LeafNode(getMostCommonClass(examples, className))
#
# argmax = remainingAttributes[0]
# gain = gainFunc(examples, argmax, attributeValues[argmax], className)
# for attribute in remainingAttributes:
#     attrGain = gainFunc(examples, attribute, attributeValues[attribute], className)
#     if gain < attrGain:
#         argmax = attribute
#         gain = attrGain
#
# #chi
# attrCnt = getAttributeCounts(examples, argmax, attributeValues[argmax], className)
# #dict of (ac, acSum)
# acToAcSum = dict()
# for ac in attrCnt.keys():
#     acSum = 0
#     for x in attrCnt[ac].keys():
#         acSum += attrCnt[ac][x]
#     acToAcSum[ac] = acSum
#
# cc = getClassCounts(examples, className)
# dev = 0
# for ac in attrCnt.keys():
#     chi = 0
#     for x in attrCnt[ac].keys():
#         pi = attrCnt[ac][x] * 1.0
#         pih = (cc[x] / (len(examples) * 1.0)) * acToAcSum[ac]
#         chi += (pi - pih) * (pi - pih) / pih
#     dev += chi
#
# v = len(attributeValues[argmax]) - 1
# stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq,df)
# if stats.chisqprob(dev, v) > q:
#     return LeafNode(getMostCommonClass(examples, className))
#
# currAttr = list(remainingAttributes)
# for a in currAttr:
#     if a == argmax:
#         currAttr.remove(a)
#
# retNode = Node(argmax)
# mcc = getMostCommonClass(examples, className)
# # dictionary (av, subtree) for upcoming for loop
# avToStDict = dict()
# for av in attributeValues[argmax]:
#     pertEx = getPertinentExamples(examples, argmax, av)
#     st = makeSubtrees(currAttr, pertEx, attributeValues, className, mcc, setScoreFunc, gainFunc)
#     avToStDict[av] = st
# retNode.children = avToStDict
#
# return retNode