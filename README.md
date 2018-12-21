# A-Priori Algorithm

The key concept of A-Priori algorihtm is : "A item should be frequent in lower degree item sets inorder to be considered for items sets of higher degree". It utilizes f2 to implement the concept of A-Priori by considering only those 2 item sets to form item sets containing 3 items which has been verified to be frequent by f2. In the proccess to consider the 2 item sets to form 3 items sets, I have considered the associative property of set. For example: If we want to check for item set containing 3 items(O, A and B) OAB then I have considered OA and OB to be chekced in f2 which in turn forms OAB by associative property of set. In this way, the frequent item sets containing 3 items are found. The whole program can be explained as:
The main function of the A_Priori class (i.e. a_priori(self, filename)) is called.
First an appropirate threshold is chosen.
It then calls the get_baskets(self, filename) method to create baskets from the retail.txt file by considering each row as a single basket. So, it returns a list containing all the basket which is referred as baskets.
Then, fis1(self, baskets, threshold) is called to get a list containing frequent item set with one item which is above the threshold frequency.
As now we have frequent item set containing 1 item, we pass it to the next function fis2(self, baskets, f1, threshold) which utilizes fis1 to take care of only those items which are in fis1(i.e. they have passed the threshold to be considered as frequent). Finally, it returns the frequent item set containing 2 items.
Similarly, to get frequent item set with 3 items, we pass the result of step 5 to fis3(self, baskets, f2, threshold) function which works in the same principle as step 5 and returns frequent item set with 3 items.



# PCY Algorithm

The PCY class uses CountPair class. Here the associative property of the A-Priori, as discussed above, is used in finding frequent item sets containing 3 items along with the Count Filter to efficeintly utilize unused memory in every phase. Count Filter is a modified form of Bloom Filter which stores frequency instead of present-absent-marker bit. In every phase, we use count filter to store frequency of pairs for successor phase. Then while implementing successor phase, in addition to the use of key concept of A-Priori algorithm, we make use of count filter to look into only those pairs which pass the threshold frequency by comparing frequency stored in count filter with the threshold. This saves us time by considering less pairs in the loop of frequent items. Hence, the PCY algorithm properly utilizes the memory as compared to A-Priori algorithm. The whole program works similar to A-Priori algorithm for each pass but the only difference is that we use count filter that contains the candidate set of items to look for in the successor pass.
