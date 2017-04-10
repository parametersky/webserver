'use strict';
export default class FileOps {
  constructor(){
    this.RNFS = require('react-native-fs');
    this.FolderPath = this.RNFS.DocumentDirectoryPath;
  }

  getFolderPath(){
    return this.FolderPath;
  }
  // static get downloadFile(url:string,path:string){
  //   var downloadoption = new DownloadFileOptions()
  //   downloadoption.toFile = path
  //   downloadoption.fromUrl =
  // }
}
// get a list of files and directories in the main bundle
// RNFS.readDir(RNFS.MainBundlePath) // On Android, use "RNFS.DocumentDirectoryPath" (MainBundlePath is not defined)
