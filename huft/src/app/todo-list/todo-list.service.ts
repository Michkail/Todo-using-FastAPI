import { HttpClient, HttpResponse } from '@angular/http';
import { Injectable } from '@angular/core';

@Injectable()
export class TodoListService {
  private resourceUrl = 'http://localhost:8000/todos';

  constructor(private http: HttpClient) { }
}
