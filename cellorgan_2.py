
class Mitochondria() :
    def __init__ (self, adp = 800, atp = 200) :
        self.adp = adp
        self.atp = atp
        self.pyruvate = 0
        self.intramem_h = 10000
        self.intracell_h = 10000
        self.nadh = 100
        self.nad = 10000
        self.fadh = 100
        self.fad = 10000
        self.tca_rate = 2
        self.etc_rate = 2
        self.atp_rate = 28  #default : tca:etc:atp = 2:2:28
        self.mashuttle_rate = 2
        self.g3pshuttle_rate = 2

    def set_mashuttle_rate (self, rate : int) :
        """
        set how many nadh tossed per frame by mashuttle
        """
        self.mashuttle_rate = rate

    def set_g3pshuttle_rate (self, rate: int) :
        """
        set how many fadh tossed per frame by g3pshuttle
        """
        self.g3pshuttle_rate = rate

    def set_total_rate(self, rate: int) :
        """
        set mitochondrial metabolism rate as a whole,
        keeping ratio at 1:1:14 for tca/etc/atp
        """
        self.tca_rate = rate
        self.etc_rate = rate
        self.atp_rate = 14 * rate

    def set_tca_rate(self, rate : int) :
        """
        set rate of TCA cycle
        """
        self.tca_rate = rate

    def set_etc_rate(self, rate : int) :
        """
        set rate of ETC, 5*rate for nadh
        """
        self.etc_rate = rate

    def set_atp_rate(self, rate : int) :
        """
        set rate of atp synthase
        default is 28 per a glucose
        """
        self.atp_rate = rate

    def get_pyruvate (self) :
        """
        returns self.pyruvate
        """
        return self.pyruvate

    def get_atp (self) :
        return self.atp

    def get_adp (self) :
        return self.adp

    def adp_to_atp (self, num) :
        """
        adp -= num
        atp += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.adp -= num
        self.atp += num

    def nad_to_nadh (self, num) :
        """
        nad -= num
        nadh += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.nad -= num
        self.nadh += num

    def fad_to_fadh (self, num) :
        """
        fad -= num
        fadh += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.fad -= num
        self.fadh += num

    def h_to_intramem (self, num) :
        """
        intracell_h -= num
        intramem_h += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.intracell_h -= num
        self.intramem_h += num

    def atp_translocase(self, num) :
        """
        num of adp/atp transported, adp to mitochondria and vice versa
        if number is negative, atp to mitochondria and vice versa
        if num exceeds mitochondrial atp/adp available, transports only until the maximum
        returns actually transported adenine number
        SHOULD ONLY BE USED BY HOST CELL
        """
        if num > self.atp :
            transported = self.atp
            self.adp += self.atp
            self.atp = 0
            return transported
        elif num < -self.adp :
            transported = self.adp
            self.atp += self.adp
            self.adp = 0
            return transported
        else :
            self.adp_to_atp(-num)
            return num

    def g3pshuttle (self) :
        """
        cell nadh to mitochondria fadh,
        if fad is not enough, returns how many transfered
        rate is determined by g3pshuttle_rate
        """
        if self.g3pshuttle_rate > self.fad :
            transported = self.fad
            self.fad_to_fadh(self.fad)
            return transported
        else :
            self.fad_to_fadh(self.g3pshuttle_rate)
            return self.g3pshuttle_rate

    def mashuttle (self) :
        """
        cell nadh to mitochondria nadh,
        if nad is not enough, returns how many transfered
        ratio is determined by mashuttle_rate
        """
        remnant = int((self.nad + self.nadh)/701)
        if self.mashuttle_rate + remnant > self.nad :
            transported = self.nad - remnant
            self.nad_to_nadh(self.nad - remnant)
            return transported
        else :
            self.nad_to_nadh(self.mashuttle_rate)
            return self.mashuttle_rate

    def pyruvate_translocase (self, num) :
        """
        add num of pyruvate to the mitochondria
        returns transfered number
        SHOULD BE USED BY HOST CELL
        """
        self.pyruvate += num
        return num

    def tca_cycle (self, num) :
        """
        num of cycle done;
        if any substrates are insufficient, it stops
        this includes oxidative decarboxylation of pyruvate -> nadh
        """
        for _ in range(num) :
            if self.pyruvate >= 1 and self.adp >= 1 and self.nad >=3 and self.fad >= 1 :
                self.pyruvate -= 1
                self.adp_to_atp(1)
                self.nad_to_nadh(4)
                self.fad_to_fadh(1)
            else :
                break

    def etc (self, nadh, fadh) :
        """
        consumes num of nadh/fadh respectively
        stops when nadh or fadh or intracell_h are insufficient
        """
        remnant_n = int((self.nad + self.nadh)/700)
        remnant_f = int((self.fad + self.fadh)/700)
        if self.nadh > 0 and self.nadh - remnant_n < nadh and self.intracell_h > 10*self.nadh :
            self.h_to_intramem(10*(self.nadh-remnant_n))
            self.nad_to_nadh(-self.nadh+remnant_n)
        elif nadh <= self.nadh and self.intracell_h > 10*nadh:
            self.h_to_intramem(10*nadh)
            self.nad_to_nadh(-nadh)

        if self.fadh > 0  and self.fadh - remnant_f < fadh and self.intracell_h > 6*self.fadh:
            self.h_to_intramem(6*(self.fadh-remnant_f))
            self.fad_to_fadh(-self.fadh+remnant_f)
        elif fadh <= self.fadh and self.intracell_h > 6*fadh :
            self.h_to_intramem(6*fadh)
            self.fad_to_fadh(-fadh)
               
    def atp_synthase (self, num) :
        """
        Makes num of ATPs, consuming 4 protons per ATP
        if no proton gradient or ADP available, stops
        """
        for _ in range(num) :
            if self.adp >= 1 and self.intramem_h >= 4 + self.intracell_h :
                self.adp_to_atp(1)
                self.h_to_intramem(-4)
            else :
                break

    def update(self) :
        self.tca_cycle(self.tca_rate)
        self.etc(5*self.etc_rate,self.etc_rate)
        self.atp_synthase(self.atp_rate)

class Ribosome() :
    def __init__(self, host : dict) :
        """
        host: a dictionary to return complete products
        host dict should be { (protein name) : (num of protein)}
        """
        self.recipe_dict = {}
        self.wait_list = {}
        self.host_dict = host
        self.atp_total = 0

    def give_atp(self, num) :
        """
        transfer num of atp to this ribosome
        only receives when there is anything left in the waiting list
        returns received atp num
        """
        if len(self.wait_list) :
            self.atp_total += num
            return num
        else :
            return 0

    def mrna(self, name : 'class', atp_consume : int) :
        """
        adds a 'name' to the waiting list
        if the same protein with different atp value is added,
        the atp needed to make the protein will be overwritten in the dictionary
        will not append if the same protein is already in the waiting list
        """
        self.recipe_dict[name] = atp_consume
        if not name in self.wait_list :
            self.wait_list[name] = 0

    def get_waitlist(self) :
        """
        returns a copy of the waiting list
        """
        return self.wait_list.copy()

    def update(self) :
        l = len(self.wait_list)
        made = []
        if l :
            for pt in self.wait_list :
                self.wait_list[pt] += self.atp_total/l
                if self.wait_list[pt] > self.recipe_dict[pt] :
                    if self.host_dict.get(pt, False) :
                        self.host_dict[pt] += 1
                    else :
                        self.host_dict[pt] = 1
                    made.append(pt)
            for pt in made:
                self.wait_list.pop(pt)
            self.atp_total = 0

class Mitochondria_easy() :
    def __init__(self) :
        """
        perfect mitochondria, fixed atp/adp
        infinite atp production
        infinite pyruvate capacity
        """
        self.atp = 200
        self.adp = 800
        self.intramem_h = 10000
        self.intracell_h = 10000
        self.nadh = 100
        self.nad = 10000
        self.fadh = 100
        self.fad = 10000
        self.tca_rate = 2
        self.etc_rate = 2
        self.atp_rate = 28  #default : tca:etc:atp = 2:2:28
        self.mashuttle_rate = 2
        self.g3pshuttle_rate = 2
        self.pyruvate = 0


    def get_atp(self):
        return self.atp

    def get_adp(self):
        return self.adp

    def atp_translocase(self,num) :
        return num

    def pyruvate_translocase (self,num) :
        return num

    def get_pyruvate(self):
        return self.pyruvate

    def mashuttle(self) :
        return self.mashuttle_rate

    def g3pshuttle(self) :
        return self.g3pshuttle_rate

    def update(self):
        pass