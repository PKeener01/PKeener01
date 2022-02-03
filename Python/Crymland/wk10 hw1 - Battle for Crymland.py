# Written by Patrick Keener on 11/18/2020
# Video Link:  https://youtu.be/B_znyCjscQs
# Honor Statement:  "I have not given or received any unauthorized assistence 
#                    on this assignment"
#
# DSC 430: Python Programming
# Assignment 1001: battle for Crymland
#
#
# This code operates using a series of classes that are called by functions
#
# recordBook class:  This class stores global imported settings as well as holds
# the other class objects in data structures that are required to run the game.
# This includes data structures that hold a series of objects that contain:  
#  1. All active Thieves, 
#  2. thieves to be promoted at the end of the turn, 
#  3. all thieves to be arrested at the end of this turn,
#  4. All detectives in-play, 
# 
# thief class: super class for lieutenant class and mrBigg.  This class initializes
# each thief and allows it to perform its duties.  Contains reference to its 
# LT's/boss's object
# 
# Lieutenant class: sub-class of thief.  Collects money and passes up to boss. 
# also promotes thieves and maintains a list of all thieves/LTs below them plus
# their own LT/boss.
#
# mrBigg class: holds all of the passed up money and does not pass it on. 
# bribes originate here.
#
# Detective class: investigates thieves, can be bribed.


import random


class recordBook():
    """ Record Book containing information used to drive the program """
    def __init__(self, settings):
        """ Record Book containing information used to drive the program """
        # ===== Record Settings =====
        # The number of thieves initially created
        self.nThieves = settings['n_thieves'] 

        # The base $/heist
        self.heistCoef = settings['heist_coef'] 
        
        # $ needed for thief to promo to lieutenant
        self.promoWealth = settings['promotion_wealth'] 

        # num of thieves each lieutenant creates
        self.lieutThieves = settings['lieut_thieves'] 

        # number of detectives created at start
        self.nDetectives = settings['n_detectives']

        # initial probability of heist solve for each detective 
        self.initSolvProb = settings['solve_init'] 

        # The maximum % probability of solving a heist
        self.capSolvProb = settings['solve_cap'] 

        # number of witnesses needed to take down a lieutenant
        self.numWitnessNeeded = settings['witnesses_needed'] 

        # The amt a detective needs to seize to get first bribe
        self.detBribeStart = settings['seize_init'] 

        # Amount of money between additional bribe attempts
        self.detBribeIncrement = settings['seize_increment'] 
        
        # Initial probability of bribing
        self.initBribeAmt = settings['bribe_init'] 

        # likelyhood a bribed detective is discovered
        self.discoverProb = settings['det_discover_prob'] 

        # Number of weeks in simulation
        self.weeks = settings['weeks'] 

        # Track if Monte Carlo is active
        self.monteCarlo = False

        
        # ===== Set Attributes ====
        
        # Attributes used to store interesting info
        self.bribesAccepted = 0 # Total amount of bribes accepted
        self.disgracedDetectives = 0 # detectives caught taking bribes
        self.activeBribedDetectives = 0 # Number of active bribed detectives
        self.numThieves = 0 # Current number of actives thieves
        self.activeLTs = 0 # Current number of actives lieutenants
        self.numJailedThieves = 0 # Thieves in jail
        self.numJailedLTs = 0 # LT in jail
        self.lootStolen = 0 # Total loot stolen- fun facts

        # attributes used in program operation
        self.outcome = 'ongoing' # Current outcome of the simulation
        self.curWeek = 0 # Current week
        self.activeThieves = set()  # List of active thieves
        self.promoList = list() # List of thieves to be promoted
        self.thiefArrestList = list() # List of thieves to be arrested
        
        # initialize detectives
        self.detectiveList = [detective(self) for i in range(self.nDetectives)]


    # Add The Don because we're lazy and it will make passing variables easy
    def addDon(self, theDon): self.theDon = theDon

    def advanceWeek(self):
       """ Advances the book and Don by one week """
       self.curWeek += 1
       self.promoList = list()
       self.theDon.resetEarnings()


class thief():
    """ The thief class.  Thieves bring in the dough. """
    
    def __init__(self, recordBook, boss):
        """ Initializes thief class """
        self.recordBook = recordBook
        self.recordBook.numThieves += 1
        self.boss = boss 
        self.bankAcct = 0
        self.inJail = False
        self.heistCoef = self.recordBook.heistCoef
        self.promoWealth = self.recordBook.promoWealth
        self.activateThief()

    def activateThief(self):
        """ Add thief to active list """
        self.recordBook.activeThieves.add(self)
    
    def arrestThief(self):
        """ Add thief to jailed list and remove from active; add 1 to boss's
        witness counter """
        self.inJail = True
        self.recordBook.activeThieves.remove(self)
        self.recordBook.numJailedThieves += 1

        try:
            self.boss.thieves.remove(self)
        except:
            print("couldn't remove thief from thief list")
            pass

        # Testify against boss
        self.boss.witnesses += 1
        self.boss.checkForArrest()

    def addToBank(self, amount):
        """ Add money to bank account and send half to boss """
        self.boss.addToBank(amount/2)
        self.bankAcct += amount/2
    
    def checkForPromo(self):
        """ Check if thief is promoted.  If so, add to list for promotion
        at end of turn """
        if self.bankAcct >= self.recordBook.promoWealth:
            self.recordBook.promoList.append(self)
    
    def conductHeist(self):
        """ Conducts an oceans eleven style heist """
        loot = self.recordBook.heistCoef*(random.randint(1,20)**2)
        self.recordBook.lootStolen += loot
        self.addToBank(loot)


class lieutenant(thief):
    """ The lieutenant class.  Runs the thieves... and the streets. """
    
    def __init__(self, recordBook, boss):
        """ Initializes the lieutenant class """
        self.boss = boss
        self.recordBook = recordBook
        self.inJail = False
        self.witnesses = 0

        # Create initial list of thieves
        self.thieves = [thief(recordBook, self) for i in range(self.recordBook.lieutThieves)]
        
        # Add lieutenant to active lieutenant list
        self.recordBook.activeLTs += 1
    
    def checkForArrest(self):
        """ Check to see if the lieutenant has enough witnesses to be arrested. 
            If more than x # of witnesses, arrest the lieutenant"""
        if self.witnesses >= self.recordBook.numWitnessNeeded:
            self.inJail = True
            self.recordBook.activeLTs -= 1
            self.recordBook.numJailedLTs += 1

            # Thieves that lose their boss begin reporting to next higher boss
            for thief in self.thieves:
                thief.boss = self.boss
                thief.boss.thieves.append(thief)

            # testify against boss
            self.boss.witnesses += 1
            try:
                self.boss.thieves.remove(self)
            except:
                print(" Couldn't remove LT from thief list ")
                pass
            self.boss.checkForArrest()

    def promoteThief(self, thief):
        """ Promote the thief 

        1. Add a new object (lieutenant) to this boss's list of thieves
        2. Transfer important attributes: bank acct balance & boss
        3. Remove thief from active thief list since they no longer run jobs
        
        """
        self.thieves.append(lieutenant(self.recordBook, self))
        self.recordBook.activeLTs += 1
        self.recordBook.numThieves -= 1
        self.thieves[-1].bankAcct = thief.bankAcct
        self.thieves[-1].boss = self
        self.recordBook.activeThieves.remove(thief)
        del thief
        

class mrBigg(lieutenant):
    """ Mr Bigg - the big boss.  Runs the whole town. 
    * Is a subtype of lieutenant which is a subtype of Thief

    input: recordBook
    """

    def __init__(self, recordBook):
        """ Initialize Mr Bigg """
        self.witnesses = 0
        self.bankAcct = 0
        self.weeklyEarnings = 0
        self.recordBook = recordBook
        self.recordBook.addDon(self)
        self.thieves = [thief(self.recordBook, self) for i in range(self.recordBook.nThieves)]
        self.inJail = False
        self.recordBook.activeLTs += 1
        
        # Add Back Story
        self.firstName = "Laura"
        self.lastName = "Deville"
        self.pronoun = "her"
        self.pronoun2 = "she"

        self.backStory = str("{} {}, AKA 'Mr Bigg', whose name strikes fear into the hearts of "\
            "the good and evil across the planet, was born in the terrifying land "\
            "known aa 'Ohio'. {} survived a terrifying ordeal in her childhood "\
            "which left an indelible mark on her soul.  After {} found {} "\
            "parents in the grocery store, {} dedicated {} life to crime. \n\n"\
            "Eventually, {} found her way to Crymland, a land ripe to build {} "\
            "criminal enterprise.  This is the record of her rise to power and the "\
            "brave detectives that sought justice in the name of the people of Crymville...\n\n\n"\
        .format(self.firstName, self.lastName, self.pronoun2.title(),
         self.pronoun2, self.pronoun, self.pronoun2, self.pronoun,
         self.pronoun2, self.pronoun))
    
    def addToBank(self, amount):
        """ Adds to bank account 
        Note: This method is different than thief/lieutenant as it does not pass
              any money upwards
        """
        self.weeklyEarnings += amount
        self.bankAcct += amount
    
    def resetEarnings(self):
        """ Resets weekly earnings; used in bribes """
        self.weeklyEarnings = 0

    def checkForArrest(self):
        """ Check if self is arrested """
        if self.witnesses >= self.recordBook.numWitnessNeeded:
            self.inJail = True
            self.recordBook.activeLTs -= 1
            self.recordBook.numJailedLTs += 1
            self.recordBook.outcome = 'detectives'
    
    def bribe(self, detective):
        """ Attempt to bribe a detective 
        Bribe amount is the percentage specified in input file * weekly earnings
        """

        bribeAmt = self.recordBook.initBribeAmt*self.weeklyEarnings

        if bribeAmt <= 10000: bribeProb = .05
        elif bribeAmt <= 100000: bribeProb = .10
        elif bribeAmt <= 1000000: bribeProb = .25
        else: bribeProb = .5

        if random.random() < bribeProb:
            detective.takeAccepted(bribeAmt)
        else:
            detective.nextBribeAttempt += detective.recordBook.detBribeIncrement


class detective():
    """ Detective Class """

    def __init__(self, recordBook):
        """ Initialize Detective """
        
        self.recordBook = recordBook
        self.bribed = False
        self.dollarsSeized = 0 # Dollars seized; drives bribe amount
        self.arrests = 0 # Number of arrests made by detective.  Fun stat :)
        
        # Probability of solving the case
        self.solveProb = self.recordBook.initSolvProb

        # Set the first bribe amount; this will increase by self.detBribeIncrement
        self.nextBribeAttempt = self.recordBook.detBribeStart

        # Likelihood of being discovered; starts at some setting
        self.discoveryProb = self.recordBook.discoverProb
    
    def takeAccepted(self, bribeAmt):
        """ The detective is now 'On the Take' and will no longer solve crimes """
        self.bribed = True
        self.solveProb = 0
        self.recordBook.activeBribedDetectives += 1
        self.recordBook.bribesAccepted += bribeAmt
    
    def discovered(self):
        """ Remove detectives once they've been discovered """

        # print('\nA traitor has been uncovered amongst the detectives! \n')

        # Fire this detective
        self.recordBook.detectiveList.remove(self)
        self.recordBook.activeBribedDetectives -= 1
        self.recordBook.disgracedDetectives += 1
        

        # Hire new detective to fill their spot
        self.recordBook.detectiveList.append(detective(self.recordBook))
        
        # Remove detective object to free up memory
        del self 

    def investigate(self, thief):
        """ investigate a heist """

        if random.random() < self.solveProb:
            thief.arrestThief()
            self.dollarsSeized += thief.bankAcct
            self.arrests += 1
            self.solveProb = min(self.solveProb + random.randint(1,10)/100, 
                self.recordBook.capSolvProb)
            
    def IAinvestigation(self):
        """ Internal Affairs is investigating this detective for bribery... """
        if random.random() > self.discoveryProb:
            self.discoveryProb += (random.randint(1, 20)/100)
        else:
            self.discovered()
    

def loadSettings(fpath = 'CrymlandInputs.txt'):
    """ Loads the settings file and converts it into a dictionary """
    inputs = open(fpath)
    settingsList = inputs.read().splitlines()
    inputs.close()

    settings = dict()
    
    for line in settingsList:
        setting, value = line.split(sep = '=')
        setting = setting.strip()
        value = eval(value.strip())
        settings[setting] = value

    
    return settings


def investigate(theLedger):
    """ drives the investigate phase 
    1.  Determine number of investigations which is the lesser of the number of
        the number of detectives or heists
    2.  Randomly select heists to investigate
    3.  Cycle through each investigation and assign a detective then investigate it
    4.  If the detective is bribed then activate investigation
    """

    numInvestigations = min(
        len(theLedger.detectiveList), len(theLedger.activeThieves))
    
    heistsUnderInvestigation = random.sample(theLedger.activeThieves, numInvestigations)

    for i in range(numInvestigations):
        detective = theLedger.detectiveList[i]
        detective.investigate(heistsUnderInvestigation[i])


def playThieves(theLedger):
    """ Execute Thief Actions """
    for thief in theLedger.activeThieves:
        thief.conductHeist()
    
    # Done in two separate loops to avoid creating thieves 
    # on the turn they're promoted
    theLedger.promoList = list()
    for thief in theLedger.activeThieves:
        thief.checkForPromo()
    
    for promote in theLedger.promoList:
        promote.boss.promoteThief(promote)


def bribery(theLedger):
    """ attempt to bribe each detective that does enough damage """
    for detective in theLedger.detectiveList:
        if detective.bribed == False: # Only check when detective isn't on the take
            if detective.dollarsSeized > detective.nextBribeAttempt:
                # print('Attempting to bribe detective...')

                theLedger.theDon.bribe(detective)
                # if detective.bribed == True:
                #     print('Detective Bribed! Score another for the bad guys...')
                # else:
                #     print('The detective resisted... this time.')
        else:
            detective.IAinvestigation()


def weeklyDisplayReport(theLedger):
    """ Displays weekly sim results """

    print("Thieves: {}, Lieutenants: {}, Lieutenants Promoted This Week: {}, "\
        "\nTotal Gold Taken: ${}"
    .format(len(theLedger.activeThieves), theLedger.activeLTs, 
    len(theLedger.promoList), int(theLedger.lootStolen)))
    print('Bribed Detectives: {}'.format(theLedger.activeBribedDetectives))

    print('Total Traitors uncovered: {}'.format(theLedger.disgracedDetectives))
    
    print("Mr Bigg's Witness Count: {}, Mr Bigg's Cut This Week: ${}, Mr Bigg's Stash: ${}\n"\
    .format(theLedger.theDon.witnesses, int(theLedger.theDon.weeklyEarnings), 
    int(theLedger.theDon.bankAcct)))


def initializeOutfile(outFile):
    outString = "gangstersNotJailed,gangstersJailed,mrBiggPersonalWealth,"\
        "bribesAccepted,winner"
    
    outFile.write(outString + '\n')
    outFile.flush()

    
def weeklySaveReport(theLedger, outFile):
    """ Items printed to the file for later retrieval """

    gangstersNotJailed = theLedger.numThieves + theLedger.activeLTs
    gangstersjailed = theLedger.numJailedThieves + theLedger.numJailedLTs
    
    outString = "{}, {}, {}, {}, {}".format(
        gangstersNotJailed, gangstersjailed, int(theLedger.theDon.bankAcct),
        int(theLedger.bribesAccepted), theLedger.outcome)
    outFile.write(outString +'\n')
    outFile.flush()


def detectiveVictory(theLedger):
    """ If the detectives win, show this """

    if theLedger.monteCarlo == False:
        print("\n\nThe brave detectives of Crymland have prevailed! Mr Biggs "\
        "has been arrested after {} weeks on the street!".format(theLedger.curWeek))

    # for i in range(len(theLedger.detectiveList)):
    #     detective = theLedger.detectiveList[i]
    #     print("Detective {}:  Dollars Recovered: {}  Thieves Arrested: {}"
    #     .format(i + 1, detective.dollarsSeized, detective.arrests))


def thiefVictory(theLedger):
    """ If Mr. Bigg wins, show this """

    if theLedger.monteCarlo == False:
        print("\n\nAfter {} weeks {} 'Mr Bigg' {} retires to a secluded isle "\
            "in a nonextradition country. \nTotal Earnings: ${}"\
            .format(theLedger.curWeek, theLedger.theDon.firstName, 
            theLedger.theDon.lastName, int(theLedger.theDon.bankAcct)))


# ===== victory() function is new since the video was recorded ===== 
# Added this code to make code more streamlined and extensible, as well as to
# more closely conform to the single responsibility principle
def victory(theLedger):
    """" Calls the victory outcomes """
    if theLedger.outcome == 'detectives':
        detectiveVictory(theLedger)
    elif theLedger.outcome == 'mrBigg':
        thiefVictory(theLedger)
    else:
        print('Victory declared out of turn.')
    

# ===== takeTurn() function is new since the video was recorded ===== 
# Added this code to make code more streamlined and extensible, as well as to
# more closely conform to the single responsibility principle
def takeTurn(theLedger):
    """ Advances the turn """

    theLedger.advanceWeek() # advance week counter, reset weekly lists

    playThieves(theLedger) # Conduct thief actions
    investigate(theLedger) # Detectives investigate thieves
    bribery(theLedger) # Mr Bigg attempts to bribe the detectives


def cleanup(theLedger):
    """ Cleanup to keep resources free during MC runs """

    for detective in theLedger.detectiveList: del detective
    for thief in theLedger.activeThieves: del thief
    del theLedger

def crymland(inPath = 'CrymlandInputs.txt', outPath = 'CrymlandStatistics.txt'):
    """ Runs the Crymland simulation """
    
    displayWeeklyReport = False # Whether to show the user a weekly printout
    monteCarlo = False # Will remove all printing


    #inPath = 'CrymlandInputs.txt' # settings file input
    #outPath = 'CrymlandStatistics.txt' # output file path
    outFile = open(outPath, 'w') # Open the file
    initializeOutfile(outFile)

    settings = loadSettings(inPath)
    theLedger = recordBook(settings)
    theDon = mrBigg(theLedger)

    theLedger.monteCarlo = monteCarlo

    if theLedger.monteCarlo == False: print(theDon.backStory)
    


    # Cycle through the designated number of weeks
    for i in range(theLedger.weeks):
        takeTurn(theLedger)

        if displayWeeklyReport == True:
            weeklyDisplayReport(theLedger) # print weekly report

        if theDon.inJail == False and (i + 1) == theLedger.weeks:
            theLedger.outcome = "mrBigg"
    
        weeklySaveReport(theLedger, outFile) # Output weekly results to file

        # Check if the Don has been arrested
        if theDon.inJail == True:
            victory(theLedger) # outcome is updated in the mrBigg class
            break
            
    if theDon.inJail == False:
        victory(theLedger)
    
    if theLedger.monteCarlo == True: cleanup(theLedger)
    
    outFile.close()

#crymland()

def monteCarlo():
    """ Runs a Monte Carlo on the simulation """

    runs = 1

    for i in range(runs):
        outPath = ('outputs\CrymlandStatistics_{}.txt'.format(i + 1))
        crymland(outPath = outPath)

    print('{} simulations have been completed'.format(runs))



    return None

monteCarlo()

def testLoadSettings(settings):
    """ test load settings function """
    print(settings)

def testtheLedger(theLedger):
    print(theLedger.nThieves)
    print(theLedger.heistCoef)
    print(theLedger.promoWealth)
    print(theLedger.lieutThieves)
    print(theLedger.nDetectives)
    print(theLedger.initSolvProb)
    print(theLedger.capSolvProb)
    print(theLedger.detBribeStart)
    print(theLedger.detBribeIncrement)
    print(theLedger.initBribeProb)
    print(theLedger.detDiscover)
    print(theLedger.weeks)

def testBankAcct(theLedger):
    theDon = mrBigg(theLedger)
    for thief in theDon.thieves:
        thief.addToBank(100)
        print(thief.bankAcct)
        print(theDon.bankAcct)
    
def testing():
    settings = loadSettings()
    theLedger = recordBook(settings)

    # testLoadSettings(settings)
    # testtheLedger(theLedger)
    # testBankAcct(theLedger)


# testing()
