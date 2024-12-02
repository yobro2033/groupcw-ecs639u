export interface Request {
    id: string;
    profile_image: string;
    first_name: string;
    last_name: string;
    email: string;
  }
  
  export interface Friend {
    id: string;
    profile_image: string;
    first_name: string;
    last_name: string;
    email: string;
  }

  export interface UserProfile {
    profile_image: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: string;
    hobbies: Hobby[];
  }
  
  export interface Hobby {
    id: string;
    name: string;
  }
  
  export interface User {
    id: string;
    profile_image: string;
    first_name: string;
    last_name: string;
    email: string;
    common_hobby_count: number;
    isFriend: boolean;
    hasSentRequest: boolean;
    hasPendingRequest: boolean;
  }