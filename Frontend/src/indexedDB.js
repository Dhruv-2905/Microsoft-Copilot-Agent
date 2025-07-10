import { openDB, deleteDB } from "idb";

const DB_NAME = "responsesDB";
const STORE_NAME = "responsesStore";

const initDB = async () => {
  return openDB(DB_NAME, 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, {
          keyPath: "id",
          autoIncrement: true,
        });
      }
    },
  });
};

const resetDBOnPageLoad = async () => {
  await deleteDB(DB_NAME);
  await initDB();
};

resetDBOnPageLoad();

export const addResponse = async (response) => {
  const db = await initDB();
  await db.add(STORE_NAME, { text: response });
};

export const getResponses = async () => {
  const db = await initDB();
  return db.getAll(STORE_NAME);
};
