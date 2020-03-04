package info.camposha.firebaserecyclerimagesuploaddownload.View;



import android.Manifest;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;

import android.widget.ImageView;
import info.camposha.firebaserecyclerimagesuploaddownload.R;
import android.widget.Button;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import android.location.Location;
import android.widget.TextView;


import com.google.android.gms.tasks.OnSuccessListener;

public class MainActivity1 extends AppCompatActivity {

    private ImageView mimageview;
    private static final int Request_Image_Capture = 101;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.takeapicture);
        mimageview = findViewById(R.id.imageview);


//
        requestPermission();
        client = LocationServices.getFusedLocationProviderClient(this);
//
        Button button = findViewById(R.id.getLocation);
        button.setOnClickListener (new View.OnClickListener(){
            @Override
            public void onClick(View view){
//                if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, android.Manifest.permission)


                client.getLastLocation().addOnSuccessListener(MainActivity1.this, new OnSuccessListener<Location>() {
                    @Override
                    public void onSuccess(Location location) {
                        if (location != null){
                            TextView textView = findViewById(R.id.location);
                            textView.setText(location.toString());


                        }

                    }
                });
            }
        });
    }

    private void requestPermission(){
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
    }
    public void TakePicture(View view)
    {
        Intent imageTakeIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (imageTakeIntent.resolveActivity(getPackageManager())!=null)
        {
            startActivityForResult(imageTakeIntent,Request_Image_Capture);
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        if (requestCode==Request_Image_Capture && resultCode==RESULT_OK)
        {
            Bundle extras = data.getExtras();
            Bitmap imageBitmap = (Bitmap) extras.get("data");
            mimageview.setImageBitmap(imageBitmap);
        }
    }
    private FusedLocationProviderClient client;

//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_main);
//        client = LocationServices.getFusedLocationProviderClient(this);
//
//        Button button = findViewById(R.id.getLocation);
//        button.setOnClickListener (new View.OnClickListener(){
//            @Override
//            public void onClick(View view){
////                if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, android.Manifest.permission)
//
//
//                client.getLastLocation().addOnSuccessListener(MainActivity1.this, new OnSuccessListener<Location>() {
//                    @Override
//                    public void onSuccess(Location location) {
//
//                    }
//                });
//            }
//        });
//    }
}
