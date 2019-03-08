from utils import *
import numpy as np



class pyDIMA:

    #Initialize DIMA, sample spatial variations
    def __init__(self, B=4,Vt=0.44,Vt_var=0.015,Nrow=512,Cblc=0.56e-15,Ncol=256,Vpre = 1,T0 = 300e-12):
        self.__B = B
        self.__Ncol = Ncol
        self.__Nrow = Nrow
        self.__Cblc = Cblc
        self.__T0 = T0
        self.__Vt_mean = Vt
        self.__Vt_var = Vt_var
        self.__Vpre = Vpre
        self.__Vt = np.random.normal(self.__Vt_mean, self.__Vt_var, (int(Ncol/2),B))

    def reset_Vt(self,Vt,Vt_var):
        self.__Vt_mean = Vt
        self.__Vt_var = Vt_var
        self.__Vt = np.random.normal(self.__Vt_mean, self.__Vt_var, (int(Ncol/2),B))

    def printVt(self):
        print(self.__Vt)


    def printVtShape(self):
        print(self.__Vt.shape)


    def FR(self,W,Vwl,model):
        """This function returns the distribution of Vbl
        """
        n = int(self.__Ncol/2)
        Vbl = np.zeros(n)
        CBL = self.__Cblc*self.__Nrow
        tao = r0*CBL
        Tr = self.__T0/5

        I_linear = 0.0
        I_sqrt = 0.0
        I_exp = 0.0

        for i in range(0,n):

            binaryWeight = decToBi(W[i],B)
            for k in range(0,self.__B):
                Ti = (self.__T0*(2**k)-2*Tr)*binaryWeight[B-k-1]

                if (Vwl-self.__Vt[i][k])<=0:
                    I_linear = 0
                    I_sqrt = 0
                else:
                    I_linear = W_L_N * KN * (Vwl-self.__Vt[i][k]) ** ALPHA
                    I_sqrt = ((Vwl-self.__Vt[i][k]) ** 1.1) * 2.5 * 80 * 1e-6



                if model == "linear":

                    Vbl[i] += I_linear/(CBL)*Ti

                elif model =="exp":
                    I_exp = I0-VDSAT/r0
                    Vbl[i] += (Vpre+ I_exp*r0)*(1-np.exp(-Ti/tao))

                elif model =="sqrt":
                    Vbl[i] += I_sqrt/(CBL)*Ti

        return Vbl


    def predict(self,Vwl,W,X,model):
        """This function returns the predicted labels given trained weight W and input X
        """
        n = 128
        sign = np.sign(W)
        W_ = np.absolute(W)

        #Function read
        Vbl = self.FR(W_,Vwl,model)

        #Add the sign
        for i in range(0,n):
            Vbl[i]=Vbl[i]*sign[i]

        y_pred = np.matmul(Vbl,X.transpose())
        y_pred=np.sign(y_pred)

        return y_pred,Vbl
