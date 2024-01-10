from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from ctypes import *
import abc

class License (SpireObject) :
    """
    Represents a license object.
    """
    @staticmethod
    def SetLicenseFileFullPathByDLLHander(dllhander, licenseFileFullPath:str):
        """
        Sets the license file full path using the DLL handler.

        Args:
            dllhander: The DLL handler.
            licenseFileFullPath: The license file full path.
        """
        licenseFileFullPathPtr = StrToPtr(licenseFileFullPath)
        if dllhander != None:
            dllhander.LISetLicenseFileFullPath.argtypes=[ c_char_p]
            dllhander.LISetLicenseFileFullPath(licenseFileFullPathPtr)
    @staticmethod
    def SetLicenseFileFullPath(licenseFileFullPath:str):
        """
        Provides a license by a license file path, which will be used for loading license.

        Args:
            licenseFileFullPath: The license file full path.
        """
        licenseFileFullPathPtr = StrToPtr(licenseFileFullPath)
        License.SetLicenseFileFullPathByDLLHander(GetDllLibDoc(), licenseFileFullPathPtr)

    @staticmethod
    def SetLicenseKey(key:str):
        """
        Provides a license by a license key, which will be used for loading license.

        Args:
            key: The value of the Key attribute of the element License of your license xml file.
        """
        keyPtr = StrToPtr(key)
        License.SetLicenseKeyByDLLHander(GetDllLibDoc(), keyPtr)

    @staticmethod
    def SetLicenseFileStream(stream:Stream):
        """
        Provides a license by a license stream, which will be used for loading license.

        Args:
            stream: The license data stream.
        """
        License.SetLicenseFileStreamByDLLHander(GetDllLibDoc(), stream)
        
    @staticmethod
    def SetLicenseFileName(licenseFileName:str):
        """
        Sets the current license file name.

        Args:
            licenseFileName: The license file name. The default license file name is [license.elic.xml].
        """
        licenseFileNamePtr = StrToPtr(licenseFileName)
        License.SetLicenseFileNameByDLLHander(GetDllLibDoc(), licenseFileNamePtr)

    @staticmethod
    def SetLicenseFileNameByDLLHander(dllhander, licenseFileName:str):
        """
        Sets the license file name using the DLL handler.

        Args:
            dllhander: The DLL handler.
            licenseFileName: The license file name.
        """
        licenseFileNamePtr = StrToPtr(licenseFileName)
        if dllhander != None:
            dllhander.LISetLicenseFileName.argtypes=[ c_char_p]
            dllhander.LISetLicenseFileName(licenseFileNamePtr)

    

    @staticmethod
    def SetLicenseFileStreamByDLLHander(dllhander, stream:Stream):
        """
        Sets the license file stream using the DLL handler.

        Args:
            dllhander: The DLL handler.
            stream: The license data stream.
        """
        if dllhander != None:
            intPtrobj:c_void_p = stream.Ptr
            dllhander.LISetLicenseFileStream.argtypes=[ c_void_p]
            dllhander.LISetLicenseFileStream( intPtrobj)

    

    @staticmethod
    def SetLicenseKeyByDLLHander(dllhander, key:str):
        """
        Sets the license key using the DLL handler.

        Args:
            dllhander: The DLL handler.
            key: The license key.
        """
        keyPtr = StrToPtr(key)
        if dllhander != None:
            dllhander.LISetLicenseKey.argtypes=[ c_char_p]
            dllhander.LISetLicenseKey(keyPtr)

    @staticmethod
    def ClearLicense():
        """
        Clears all cached licenses.
        """
        License.ClearLicenseByDLLHander(GetDllLibDoc())

    @staticmethod
    def ClearLicenseByDLLHander(dllhander):
        """
        Clears all cached licenses using the DLL handler.

        Args:
            dllhander: The DLL handler.
        """
        if dllhander != None:
            dllhander.LIClearLicense( )


    @staticmethod
    def LoadLicense():
        """
        Loads the license provided by the current setting to the license cache.
        """
        License.LoadLicenseByDLLHander(GetDllLibDoc())

    @staticmethod
    def LoadLicenseByDLLHander(dllhander):
        """
        Loads the license using the DLL handler.

        Args:
            dllhander: The DLL handler.
        """
        if dllhander != None:
            dllhander.LILoadLicense( )
  #  @staticmethod
  #  def GetLicenseFileName()->str:
  #      """
		#<summary>
		#    Gets the current license file name.
		#</summary>
		#<returns>The license file name, the default license file name is [license.elic.xml].</returns>
  #      """
  #      ret = License.GetLicenseFileNameByDLLHander(GetDllLibDoc())
  #      if ret == None:
  #          ret = License.GetLicenseFileNameByDLLHander(GetDllLibPdf())
  #      if ret == None:
  #          ret = License.GetLicenseFileNameByDLLHander(GetDllLibXls())
  #      if ret == None:
  #          ret = License.GetLicenseFileNameByDLLHander(GetDllLibPpt())
  #      return ret
    @staticmethod
    def GetLicenseFileNameByDLLHander(dllhander)->str:
        """
        Gets the current license file name using the DLL handler.

        Args:
            dllhander: The DLL handler.

        Returns:
            The license file name. The default license file name is [license.elic.xml].
        """
        if dllhander != None:
            dllhander.LIGetLicenseFileName.argtypes=[c_void_p]
            return dllhander.LIGetLicenseFileName( )
        return None
