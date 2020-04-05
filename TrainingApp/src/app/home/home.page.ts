import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
declare var WifiWizard2: any;
declare var WifiWizard: any;
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  results = [];
  info_txt = '';
  async getNetworks() {
    this.info_txt = 'loading...';
    try {
      let results = await WifiWizard2.scan();
      this.results = results;
      this.info_txt = '';
    } catch (error) {
      this.info_txt = error;
    }
  }
}
