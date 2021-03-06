import { Injectable } from '@angular/core';
import {
  AngularFirestore,
  AngularFirestoreCollection,
  AngularFirestoreDocument,
  DocumentReference,
} from '@angular/fire/firestore';
import { map, take } from 'rxjs/operators';
import { Observable } from 'rxjs';

export interface Data {
  id?: string;
  x: number;
  y: number;
}

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private ideas: Observable<Data[]>;
  private ideaCollection: AngularFirestoreCollection<Data>;
  customersRef: AngularFirestoreCollection<Data> = null;
  constructor(private afs: AngularFirestore) {
    this.ideaCollection = this.afs.collection<Data>('Data');
    this.ideas = this.ideaCollection.snapshotChanges().pipe(
      map((actions) => {
        return actions.map((a) => {
          const data = a.payload.doc.data();
          const id = a.payload.doc.id;
          return { id, ...data };
        });
      })
    );
  }
  getList(): AngularFirestoreCollection<Data> {
    return this.customersRef;
  }
  getIdeas(): Observable<Data[]> {
    return this.ideas;
  }

  getIdea(id: string): Observable<Data> {
    return this.ideaCollection
      .doc<Data>(id)
      .valueChanges()
      .pipe(
        take(1),
        map((idea) => {
          idea.id = id;
          return idea;
        })
      );
  }

  addIdea(idea: Data): Promise<DocumentReference> {
    return this.ideaCollection.add(idea);
  }
}
