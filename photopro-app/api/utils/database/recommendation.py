import psycopg2

num_related_photos=3

def get_terms_and_values_for_image(image_id, conn, cur):
    try:
        cmd = "select term, value from auto_tags where image_id={} ORDER by value DESC".format(int(image_id))
        cur.execute(cmd)
        conn.commit()
        result = cur.fetchall()

        if len(result) == 0:
            return False
        else:
            return result

    except psycopg2.Error as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False
    except Exception as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False


def update_recommendation_term(user_id, term, value, coefficient, conn, cur):
    try:
        cmd = "select value from recommendations where user_id={} AND term ILIKE '{}'".format(int(user_id), term)
        cur.execute(cmd)
        print(cmd)
        conn.commit()

        result = cur.fetchone()
        print(result)
        if result is not None:
            new_value = float(result[0]) + value * coefficient
            cmd = (
                "UPDATE recommendations SET value={} WHERE user_id={} AND term='{}'".format(
                    new_value, int(user_id), term
                )
            )
        else:
            new_value = value
            cmd = (
                "INSERT INTO RECOMMENDATIONS (user_id, term, value) VALUES ({}, '{}', {})".format(
                    int(user_id), term, new_value
                )
            )


        cur.execute("SAVEPOINT save_point")
        print(cmd)
        cur.execute(cmd)
        conn.commit()

        return result

    except psycopg2.Error as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False
    except Exception as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False

def get_recommendation_photos(user_id, conn, cur):
    try:
        cmd = "select image_id, title FROM images WHERE \
                lower(ARRAY['Ocean','panda']::text)::text[] && \
                lower(tags::text)::text[] AND uploader!={}".format(int(user_id))
        # "select image_id, count(*) from images, unnest(array['Ocean', 'Panda'])\
        #  u where tags @> array[u] group by image_id ORDER BY 2 DESC, 1;"
        cur.execute(cmd)
        conn.commit()
        result = cur.fetchall()

        if len(result) == 0:
            return False
        else:
            return result

    except psycopg2.Error as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False
    except Exception as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False

def get_related_images(image_id,num_images,conn,cur):
    try:
        cmd="select img_id,count(tag) from images_with_common_tags({}) GROUP BY img_id ORDER BY count DESC LIMIT {}".format(image_id,num_images)
        cur.execute(cmd)
        conn.commit()
        result = cur.fetchall()
        num_img_found=len(result)
        print("input image id")
        print(image_id)
        print("")
        print("number of related images")
        print(num_img_found)
        print("")
        for img_id,count in result:
            print("related image id:")
            print(img_id)
            print("num of matching tags:")
            print(count)
            print("")

    except psycopg2.Error as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False
    except Exception as e:
        print(e)
        # cur.execute('ROLLBACK TO SAVEPOINT save_point')
        return False
